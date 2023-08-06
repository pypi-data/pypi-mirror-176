import logging
import sys
import time
from datetime import datetime
from functools import partial
from typing import Dict, Optional, Tuple, TypedDict

try:
    import botostubs
except ImportError:
    pass
import boto3  # type: ignore
import botocore  # type: ignore
from botocore.credentials import RefreshableCredentials  # type: ignore
from botocore.session import get_session  # type: ignore

DEFAULT_REGION = "us-east-1"
TTL = 900
logger = logging.getLogger(__name__)


class Credentials(TypedDict):
    access_key: str
    secret_key: str
    token: str
    expiry_time: str


CacheKey = Tuple[str, str, str, Optional[str]]
CacheEntry = Tuple[int, Credentials]
CACHE: Dict[CacheKey, CacheEntry] = dict()


def _write_to_stderr(msg, newline="\n"):
    sys.stderr.write(msg + newline)
    sys.stderr.flush()


def _get_profile_credentials(
    profile_name: str, sts_region: str = DEFAULT_REGION, refreshing: bool = False
) -> Credentials:
    if refreshing:
        logger.info(
            "Autorefresh profile session triggered internal credentials refresh for profile %s",
            profile_name,
        )
        _write_to_stderr(
            f"[!] Credentials for profile {profile_name} have expired.  Please update your credentials to allow this program to continue."
        )
    else:
        logger.info(
            "New session triggered credentials refresh for profile %s", profile_name
        )
    sys.stderr.flush()
    while True:
        try:
            session = boto3.Session(profile_name=profile_name)
            sts = session.client("sts", region_name=sts_region)
            sts.get_caller_identity()
        except Exception:
            if not refreshing:
                _write_to_stderr(
                    f"[!] Credentials for profile {profile_name} have expired.  Please update your credentials to allow this program to continue."
                )
            time.sleep(5)
        else:
            break
    credentials: Credentials = dict(
        access_key=session.get_credentials().access_key,
        secret_key=session.get_credentials().secret_key,
        token=session.get_credentials().token,
        expiry_time=datetime.fromtimestamp(time.time() + TTL).isoformat(),
    )
    return credentials


def _get_credentials(
    account_id: str,
    role_name: str,
    role_session_name: str,
    source_session: boto3.Session = None,
    sts_region: str = DEFAULT_REGION,
    refreshing: bool = False,
) -> Credentials:
    key = (account_id, role_name, role_session_name, sts_region)
    if refreshing:
        logger.info(
            "Autorefresh session triggered internal credentials refresh for key %s", key
        )
    else:
        logger.info("New session triggered credentials refresh for key %s", key)
    now = int(time.time())
    expiration, cached_credentials = CACHE.get(key, (0, None))
    if cached_credentials is not None and now < expiration:
        logger.info(
            "Returning cached, unexpired credentials which will expire at %s",
            expiration,
        )
        return cached_credentials
    elif cached_credentials:
        logger.info("Cache contained expired credentials. Retrieving new credentials.")
    source_session = source_session or boto3.Session()
    sts = source_session.client("sts", region_name=sts_region)
    logger.info(
        "Assuming role %s in %s region in %s account ID",
        role_name,
        sts_region,
        account_id,
    )
    response = sts.assume_role(
        RoleArn=f"arn:aws:iam::{account_id}:role/{role_name}",
        RoleSessionName=role_session_name,
    )
    expires_epoch: int = (
        int(response["Credentials"]["Expiration"].timestamp()) - 5
    )  # Five second buffer for... reasons
    credentials: Credentials = dict(
        access_key=response["Credentials"]["AccessKeyId"],
        secret_key=response["Credentials"]["SecretAccessKey"],
        token=response["Credentials"]["SessionToken"],
        expiry_time=response["Credentials"]["Expiration"].isoformat(),
    )
    CACHE[key] = (expires_epoch, credentials)
    logger.info("Returning refreshed credentials which will expire at %s", expiration)
    return credentials


def get_refreshable_profile_session(
    *, profile_name: str, sts_region: str = None
) -> boto3.session.Session:
    sts_region = sts_region or DEFAULT_REGION
    logger.info(
        "Setting up new autorefresh profile session for profile %s", profile_name
    )
    credentials = RefreshableCredentials.create_from_metadata(
        metadata=_get_profile_credentials(profile_name, sts_region=sts_region),
        refresh_using=partial(
            _get_profile_credentials,
            profile_name,
            sts_region=sts_region,
            refreshing=True,
        ),
        method="sts-assume-role",
    )
    session = get_session()
    session._credentials = credentials
    autorefresh_session = boto3.session.Session(botocore_session=session)
    return autorefresh_session


def get_autorefresh_session(
    *,
    account_id: str,
    role_name: str,
    role_session_name: str,
    source_session: boto3.Session = None,
    sts_region: str = None,
) -> boto3.session.Session:
    key = (account_id, role_name, role_session_name, sts_region)
    sts_region = sts_region or DEFAULT_REGION
    logger.info("Setting up new autorefresh session for key %s", key)
    credentials = RefreshableCredentials.create_from_metadata(
        metadata=_get_credentials(
            account_id,
            role_name,
            role_session_name,
            source_session=source_session,
            sts_region=sts_region,
        ),
        refresh_using=partial(
            _get_credentials,
            account_id,
            role_name,
            role_session_name,
            source_session=source_session,
            sts_region=sts_region,
            refreshing=True,
        ),
        method="sts-assume-role",
    )
    session = get_session()
    session._credentials = credentials
    autorefresh_session = boto3.session.Session(botocore_session=session)
    return autorefresh_session
