from pathlib import Path

try:
    import botostubs
except ImportError:
    pass


def get_accounts(session, include_ous=False, region_name="us-east-1"):
    if include_ous:
        accounts_ous = get_accounts_ous(session, region_name=region_name)
    else:
        accounts_ous = {}
    sts = session.client("sts")
    caller = sts.get_caller_identity()
    organizations = session.client("organizations", region_name=region_name)
    accounts = []
    paginator = organizations.get_paginator("list_accounts")
    for page in paginator.paginate():
        for account in page["Accounts"]:
            account_obj = {
                "account_id": account["Id"],
                "account_name": account["Name"],
                "account_email": account["Email"],
                "account_status": account["Status"],
                "mpa_account_id": caller["Account"],
                "create_or_join_date": account["JoinedTimestamp"].isoformat(),
            }
            ou_details = accounts_ous.get(account["Id"], {})
            account_obj.update(ou_details)
            tags = organizations.list_tags_for_resource(ResourceId=account["Id"])
            for tag in tags["Tags"]:
                account_obj[tag["Key"]] = tag["Value"]
            accounts.append(account_obj)
    return accounts


def get_accounts_ous(session, region_name="us-east-1"):
    organizations = session.client("organizations", region_name=region_name)
    paginator = organizations.get_paginator("list_roots")
    response = organizations.describe_organization()
    org_id = response["Organization"]["Id"]
    path = Path("")
    accounts = {}
    for page in paginator.paginate():
        for root in page["Roots"]:
            root_id = root["Id"]
            root_name = root["Name"]
            org_path_ids = path / org_id / root_id
            org_path_names = path / root_name
            get_children(
                session,
                accounts,
                root_id,
                root_name,
                org_path_ids,
                org_path_names,
                region_name=region_name,
            )
    return accounts


def get_children(
    session,
    collector,
    resource_id,
    resource_name,
    org_path_ids,
    org_path_names,
    region_name="us-east-1",
):
    organizations = session.client("organizations", region_name=region_name)
    paginator = organizations.get_paginator("list_accounts_for_parent")
    for page in paginator.paginate(ParentId=resource_id):
        for account in page["Accounts"]:
            collector[account["Id"]] = {
                "org_id": resource_id,
                "org_path_name": resource_name,
                "org_path_ids": str(org_path_ids),
                "org_path_names": str(org_path_names),
            }
    paginator = organizations.get_paginator("list_organizational_units_for_parent")
    for page in paginator.paginate(ParentId=resource_id):
        for ou in page["OrganizationalUnits"]:
            get_children(
                session,
                collector,
                ou["Id"],
                ou["Name"],
                org_path_ids / ou["Id"],
                org_path_names / ou["Name"],
                region_name=region_name,
            )
    return collector
