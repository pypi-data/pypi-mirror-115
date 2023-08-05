#! /usr/bin/python3
"""
.. py:module:: main
    :synopsis: The primary functional module for database interactions

"""

from os import name, getenv
from pathlib import Path
from tinydb import TinyDB, Query

class database:
    def __init__(self, filename):
        if name == "posix":
            path = '.local/apikeychain/'
        elif name == "nt":
            appdata = getenv('APPDATA')
            path = Path(str(f'{appdata}/apikeychain/'))
        else:
            raise NotImplementedError

        path.mkdir(parents=True, exist_ok=True)
        self.loc =  f'{path}/{filename}.db'

    def generate_db(self):
            db = TinyDB(self.loc)
            return db

    def retrieve_db(self):
        try:
            db = TinyDB(self.loc)
            return db
        except:
            raise FileNotFoundError

    def remove_db(self):
        self.unlink()

def api_store(app, key, expiration, userdata, pw, file):
    """
    .. py:function:: store(filename, application, key[, expiration][, userdata], password)
    
        :param str filename: Represents the name of the keychain. An invalid name will cancel the operation with a warning to use api-keychain init to create
        :param str application: The name of the application your key belongs to
        :param str key: The raw text of your API key to be encrypted and stored in the database
        :param expiration: An optional expiration date. Currently, there is no data validation, so any strings are valid
        :type expiration: int or None
        :param userdata: A custom set of userdata to store alongside the key
        :type userdata: Dict or None
        :param None password: The password for your keychain. The system will prompt you to enter this during operation
        :rtype: None
    """
    from .crypto import encrypt_key
    db = database(file).retrieve_db()
    try:
        enc, salt = encrypt_key(key, pw, file)
        db.insert({'application': app, 'key': str(enc), 'salt': salt, 'expiration': expiration, 'custom_data': userdata})
        return
    except:
        print('No keychain found, run api-keychain init to generate a new keychain.')
        quit()

def api_retrieve(app, pw, file):
    """
    .. py:function:: retrieve(filename, application, password)

        :param str application: The name of the application whose key you want to retrieve
        :param None password: The password for your keychain. The system will prompt you to enter this during operation
        :param str filename: Represents the name of the keychain. An invalid name will cancel the operation with a warning to use api-keychain init to create
        :return: The decrypted API key
        :rtype: str
    """
    from .crypto import decrypt_key
    db = database(file).retrieve_db()
    data = db.get(Query().application == app)
    enc = data['key']
    salt = data['salt']
    return decrypt_key(enc, pw, salt, file)