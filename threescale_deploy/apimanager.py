from typing import Dict

import openshift
from .environment import get_aws_details, get_route_prefix, get_cluster_wildcard
from . import logger


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
    aws_creds = get_aws_details()
    with openshift.project(project_name):
        if openshift.selector("secret/aws-secret").count_existing() > 0:
            return
        secret = openshift.build_secret_dict(secret_name="aws-secret")
        secret = secret | {"stringData": {"AWS_BUCKET": aws_bucket_name} | aws_creds}
        openshift.create(secret)


def create_apimanager(name: str, project: str):
    logger.info("Creating apimanager %s" % name)
    with openshift.project(project):
        objs = openshift.selector("apimanager")
        if objs.count_existing() != 0:
            logger.warning("Apimanager %s in %s already created" % (name, project))
            return objs.object()
        wildcard_domain = _resolve_wildcard_domain()
        if get_route_prefix():
            wildcard_domain = f"{get_route_prefix()}.{wildcard_domain}"
        logger.debug(f"Wildcard domain in use f{wildcard_domain}")
        apimanager = _build_apimanager(name, wildcard_domain, "aws-secret")
        return openshift.create(apimanager)


def _apimanager_installed(apimanager):
    ready = apimanager.model.status.conditions.can_match(
        {"type": "Available", "status": "True"}
    )
    return ready


def wait_for_apimanager(name: str, project: str) -> bool:
    with openshift.project(project):
        logger.info("Waiting for apimanager to become ready for 10 minutes")
        with openshift.timeout(10 * 60):
            openshift.selector(f"apimanager/{name}").until_any(
                success_func=_apimanager_installed
            )
            logger.info("Apimanager is up and ready")
        if not _apimanager_installed(openshift.selector(f"apimanager/{name}").object()):
            logger.warning("Apimanager is not ready")
            return False
        return True


def delete_apimanager(name: str, project: str):
    logger.info(f"Deleting apimanager {name} in {project}")
    with openshift.project(project):
        apimanagers = openshift.selector(f"apimanager/{name}").object()
        apimanagers.delete()
