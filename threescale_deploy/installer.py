import click
from .apimanager import create_apimanager, create_secrets, delete_apimanager
from .s3 import create_bucket, remove_bucket
from .environment import get_bucket_name, get_project_name


@click.group()
def cli():
    pass


@cli.command()
def install():
    bucket = get_bucket_name()
    project = get_project_name()
    create_bucket(bucket)
    create_secrets(bucket, project)
    create_apimanager("manager1", project)


@cli.command()
def remove():
    bucket = get_bucket_name()
    project = get_project_name()

    delete_apimanager("manager1", project)
    remove_bucket(bucket)
