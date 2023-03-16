from typing import Dict, Optional
from os import environ


def get_aws_details() -> Dict[str, str]:
    return {
        "AWS_ACCESS_KEY_ID": environ["AWS_ACCESS_KEY_ID"],
        "AWS_REGION": environ["AWS_REGION"],
        "AWS_SECRET_ACCESS_KEY": environ["AWS_SECRET_ACCESS_KEY"],
    }


def get_project_name() -> str:
    return environ["DEPL_PROJECT_NAME"]


def get_bucket_name() -> str:
    return environ["DEPL_BUCKET_NAME"]


def get_route_prefix() -> Optional[str]:
    return environ.get("DEPL_ROUTE_PREF", None)


def get_cluster_wildcard() -> Optional[str]:
    return environ.get("DEPL_CLUSTER_WILD", None)
