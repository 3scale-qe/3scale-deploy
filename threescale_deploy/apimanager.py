import openshift
from typing import Dict
from .environment import get_AWS_details, get_route_prefix, get_cluster_wildcard


def _build_apimanager(name: str, domain: str, secret_name: str) -> Dict:
    apimanager = {
        "apiVersion": "apps.3scale.net/v1alpha1",
        "kind": "APIManager",
        "metadata": {"name": name},
        "spec": {
            "wildcardDomain": domain,
            "system": {
                "fileStorage": {
                    "simpleStorageService": {
                        "configurationSecretRef": {"name": secret_name}
                    }
                }
            },
        },
    }
    return apimanager


def _resolve_wildcard_domain() -> str:
    wildcard = get_cluster_wildcard()
    if not wildcard:
        wildcard = (
            openshift.selector("ingress.v1.config.openshift.io/cluster")
            .object()
            .model.spec.domain
        )
    return wildcard


def create_secrets(aws_bucket_name, project_name):
    aws_creds = get_AWS_details()
    with openshift.project(project_name):
        secret = openshift.build_secret_dict(secret_name="aws-secret")
        secret = secret | {"stringData": {"AWS_BUCKET": aws_bucket_name} | aws_creds}
        print(secret)
        openshift.create(secret)


def create_apimanager(name: str, project: str):
    with openshift.project(project):
        wildcard_domain = _resolve_wildcard_domain()
        if get_route_prefix():
            wildcard_domain = f"{get_route_prefix()}.{wildcard_domain}"
        objs = openshift.selector("apimanager")
        if objs.count_existing() != 0:
            return None
        apimanager = _build_apimanager(name, wildcard_domain, "aws-secret")
        return openshift.create(apimanager)


def delete_apimanager(name: str, project: str):
    with openshift.project(project):
        apimanagers = openshift.selector(f"apimanager/{name}").object()
        apimanagers.delete()
