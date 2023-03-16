import logging
from typing import Tuple

import click
import coloredlogs
from openshift import OpenShiftPythonException

from .apimanager import (
    create_apimanager,
    create_secrets,
    delete_apimanager,
    wait_for_apimanager,
)
from .s3 import create_bucket, remove_bucket
from .environment import get_bucket_name, get_project_name
from . import logger, log_exception


def _install_and_set_logger(verbosity: int):
    if verbosity == 0:
        coloredlogs.install(level=logging.INFO)
    elif verbosity >= 1:
        coloredlogs.install(level=logging.DEBUG)
    if verbosity <= 1:
        logging.getLogger("botocore").setLevel(logging.WARNING)
        logging.getLogger("urllib3").setLevel(logging.WARNING)
        logging.getLogger("openshift").setLevel(logging.WARNING)


def _resolve_variables() -> Tuple[str, str]:
    try:
        bucket = get_bucket_name()
        project = get_project_name()
    except KeyError as ex:
        log_exception(f"Variable not found {ex}", logging.ERROR, ex)
        exit(-1)
    return bucket, project


@click.group()
@click.option("-v", "--verbose", count=True, help="Increase logging of the command")
def cli(verbose):
    _install_and_set_logger(verbose)


@cli.command()
def install():
    bucket, project = _resolve_variables()
    create_bucket(bucket)
    create_secrets(bucket, project)
    create_apimanager("manager1", project)
    wait_for_apimanager("manager1", project)
    logger.info("Deployer finished!")


@cli.command()
def remove():
    bucket, project = _resolve_variables()
    try:
        delete_apimanager("manager1", project)
    except OpenShiftPythonException as ex:
        log_exception(f"Unable to delete manager {ex}", logging.ERROR, ex)
    remove_bucket(bucket)
