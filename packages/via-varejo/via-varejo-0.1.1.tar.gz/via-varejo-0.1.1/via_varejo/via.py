import pymongo

from pydoc import cli
from datetime import datetime

from robot.api.logger import info, debug, trace, console, error
from robot.api.deco import keyword
from robot.api import Error


def connect_to_database(strConnction):
    try:
        client = pymongo.MongoClient(f"mongodb://{strConnction}/")

        return client
    except Exception as e:
        raise Error(e)


def disconnect_to_database(client):
    try:
        client.close()

        info("Connection has closed sucess")
    except Exception as e:
        raise Error(e)


def find_all(client, baseName, collectionName):
    try:
        lstItems = []

        dataBase = client[baseName]

        collection = dataBase[collectionName]

        result = collection.find()

        for item in result:
            lstItems.append(item)

        info(lstItems)

        return lstItems
    except Exception as e:
        raise Error(e)


def find_by_pameter(client, baseName, collectionName, parameter, value):
    try:
        dataBase = client[baseName]

        collection = dataBase[collectionName]

        for item in collection.find({parameter: value}):
            if item[parameter] == value:
                info(item)
                return item

        return None
    except Exception as e:
        raise Error(e)


def remove_by_pameter(client, baseName, collectionName, parameter, value):
    try:
        dataBase = client[baseName]

        collection = dataBase[collectionName]

        collection.delete_one({parameter: value})

        return None
    except Exception as e:
        raise Error(e)


def split_text(text, length):
    try:

        return str(text)[0: int(length)]
    except Exception as e:
        raise Error(e)