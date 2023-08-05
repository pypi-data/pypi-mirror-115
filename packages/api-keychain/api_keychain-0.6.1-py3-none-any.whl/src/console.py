#! /usr/bin/python3
'''
.. py:module:: console
    :synopsis: The primary entry-point for user interactions with the package
'''
import click
from .main import api_store, api_retrieve
from .crypto import create_password

@click.group(no_args_is_help=True)
def cli():
    pass

@cli.command()
@click.argument('filename')
@click.argument('application')
@click.argument('key')
@click.argument('expiration', required=False, default='1/1/9999')
@click.argument('userdata', required=False, default='{}')
@click.password_option('-pw', '--password')
def store(application, key, expiration, userdata, password, filename):
    '''
    Stores data in FILENAME using the included arguments.
    \f
    '''
    api_store(application,key,expiration,userdata, password, filename)

@cli.command()
@click.argument('filename')
@click.argument('application')
@click.password_option('-pw', "--password")
def retrieve(application, password, filename):
    '''Retrieve key from FILENAME tied to APPLICATION. Requires the keychain's master password.
    '''
    api_retrieve(application, password, filename)

@cli.command()
@click.argument('filename')
def init(filename):
    '''
    .. py:function:: init(filename)
        :param str filename: Represents the name of the keychain
        :param password: A password which the system will prompt for during operation
        :rtype: None
    '''
    create_password(filename)

if __name__ == '__main__':
    cli()