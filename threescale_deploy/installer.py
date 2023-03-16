import logging

import click
import coloredlogs
from openshift import OpenShiftPythonException

from .apimanager import create_apimanager, create_secrets, delete_apimanager
from .s3 import create_bucket, remove_bucket
from .environment import get_bucket_name, get_project_name
from . import logger


def _install_and_set_logger(verbosity: int):
    if verbosity == 0:
        coloredlogs.install(level=logging.INFO)
    elif verbosity >= 1:
        coloredlogs.install(level=logging.DEBUG)
    if verbosity <= 1:
        logging.getLogger('botocore').setLevel(logging.WARNING)
        logging.getLogger('urllib3').setLevel(logging.WARNING)
        logging.getLogger('openshift').setLevel(logging.WARNING)


@click.group()
@click.option("-v", "--verbose", count=True, help="Increase logging of the command")
def cli(verbose):
    _install_and_set_logger(verbose)


@cli.command()
def install():
    try:
        bucket = get_bucket_name()
        project = get_project_name()
    except KeyError as ex:
        logger.error(f"Necessary variables not set {ex}")
        exit(-1)
    create_bucket(bucket)
    create_secrets(bucket, project)
    create_apimanager("manager1", project)


@cli.command()
def remove():
    try:
        bucket = get_bucket_name()
        project = get_project_name()
    except KeyError as ex:
        logger.error(f"Necessary variables not set {ex}")
        exit(-1)

    try:
        delete_apimanager("manager1", project)
    except OpenShiftPythonException as ex:
        logger.error(f"Unable to delete manager {ex.msg}")
    remove_bucket(bucket)
