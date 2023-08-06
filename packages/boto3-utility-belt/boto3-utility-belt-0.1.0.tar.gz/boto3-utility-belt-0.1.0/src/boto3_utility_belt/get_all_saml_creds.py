import base64
import configparser
import os
import xml.etree.ElementTree as ET
from io import StringIO
from pathlib import Path

import boto3
import pyperclip


def verify_aws_folder():
    aws_folder = Path.home() / ".aws"
    try:
        os.makedirs(aws_folder)
    except FileExistsError:
        pass


def add_creds(account_id, role_name, params):
    creds_file = Path.home() / ".aws" / "credentials"
    config = configparser.ConfigParser()
    config.read(creds_file)
    config[f"{account_id}-{role_name}"] = params
    with open(creds_file, "w") as f:
        config.write(f)


def main():
    verify_aws_folder()
    session = boto3.Session(aws_access_key_id="XXXX", aws_secret_access_key="XXXX")
    client = session.client("sts", region_name="us-west-2")

    print("Copy the SAMLResponse and then hit enter...", end="")
    input()
    print("")

    saml_assertion_encoded = pyperclip.paste()
    saml_assertion = base64.b64decode(saml_assertion_encoded.encode("utf-8")).decode(
        "utf-8"
    )
    tree = ET.fromstring(saml_assertion)

    nsmap = dict(
        [
            node
            for _, node in ET.iterparse(StringIO(saml_assertion), events=["start-ns"])
        ]
    )
    role_attribute = list(
        tree.findall(
            ".//saml:Attribute[@Name='https://aws.amazon.com/SAML/Attributes/Role']",
            nsmap,
        )
    )

    roles = []
    for role in role_attribute[0].findall(".//saml:AttributeValue", nsmap):
        role_arn, principal_arn = role.text.split(", ")
        _, _, _, _, account_id, role_name = role_arn.split(":")
        role_name = role_name.split("/")[1]
        print(f"Assuming role {role_arn}...", end="")
        try:
            creds = client.assume_role_with_saml(
                RoleArn=role_arn,
                PrincipalArn=principal_arn,
                SAMLAssertion=saml_assertion_encoded,
            )
            creds_object = {
                "aws_access_key_id": creds["Credentials"]["AccessKeyId"],
                "aws_secret_access_key": creds["Credentials"]["SecretAccessKey"],
                "aws_session_token": creds["Credentials"]["SessionToken"],
            }
            add_creds(account_id, role_name, creds_object)
        except Exception:
            print("Failed")
        else:
            print("Succeeded")


if __name__ == "__main__":
    main()
