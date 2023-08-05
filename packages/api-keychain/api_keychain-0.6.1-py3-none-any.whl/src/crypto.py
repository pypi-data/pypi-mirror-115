#! /usr/bin/python3
"""
.. py:module:: crypto
    :synopsis: The module for each of the various encryption/decryption functions and their related features
"""

import base64
from tinydb import Query
from passlib.hash import pbkdf2_sha256
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from .main import database

# password management
def create_password(file):
    """
    .. py:function:: create_password(filename)
    
        :synopsis: Generates a master password for the keychain and stores a hashed version as the first database entry
        :param str filename: The name of the database file being modified
        :return: the password that was created
        :rtype: str
        :meta warning: The create_password function returns the password in plaintext, intended to be used in other functions later. This leaves a security vulnerability if the password is somehow intercepted in RAM.
    """
    from stdiomask import getpass
    db = database(file).generate_db()
    pw = getpass(prompt='Please enter a new password: ')
    pwver = getpass(prompt='Please re-enter your password: ')
    if pw == pwver:
        has = pbkdf2_sha256.hash(pw)
        db.insert({'application': 'master', 'key': has, 'expiration': '', 'custom_data': ''})
        return pw
    else:
        print('Your passwords did not match, please try again.')
        create_password(file)

def use_password(pw, file):
    """
    .. py:function:: use_password(password, filename)

        :param str password: The password for the database, either automatically provided by a previous :py:func:`create_password` call, or submitted by the user
        :param str filename: The keychain being unlocked
        :meta note: Takes the password and verifies it against the hashed password in the database.
        :return: The submitted password
        :rtype: str
        :raises RuntimeError: if the password verification fails
        :meta warning: The password is transferred around in plaintext, although verification status is not saved.
    """
    db = database(file).retrieve_db()
    has = db.get(Query().application == "master")['key']
    if pbkdf2_sha256.verify(pw, has):
        return pw
    else:
        raise RuntimeError('Invalid password')

# encryption
def encrypt_key(key, *args):
    """
    .. py:function:: encrypt_key(key, password, filename)

        :synopsis: Encryptes the API key and returns the encrypted token and salt for further use
        :param str key: the unencrypted API key
        :param str password: the keychain master password
        :param str filename: The keychain filename
        :return: the encrypted key token
        :return: the encryption salt
        :rtype: str, str
    """
    from os import urandom
    if args[0]:
        pas = use_password(args[0], args[1])
        salt = urandom(16)
        kdf = PBKDF2HMAC(algorithm=hashes.SHA256(),length=32,salt=salt,iterations=100000,)
        sec = base64.b64encode(kdf.derive(bytes(pas,'utf-8')))
        token = Fernet(sec).encrypt(bytes(key,'utf-8'))
        token = token.decode('utf-8')
        salt = base64.b64encode(salt).decode('utf-8')
        return token, salt

#decryption
def decrypt_key(token, pw, salt, file):
    """
    .. py:function:: decrypt_key(token, password, salt, filename)

    :synopsis: decrypt the api-key, using the salt and password provided. Returns the decrypted key.
    :param str token: plaintext version of the token imported from the database
    :param str pw: plaintext version of the master password
    :param str salt: plaintext version of the salt, stored alongside the key in the database
    :param str filename: name of the database file
    :return: the decrypted key
    :rtype: str
    """
    pas = use_password(pw, file)
    salt = base64.b64decode(salt)
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(),length=32,salt=salt,iterations=100000,)
    sec = base64.b64encode(kdf.derive(bytes(pas,'utf-8')))
    key = Fernet(sec).decrypt(bytes(token,'utf-8'))
    return key.decode('utf-8')