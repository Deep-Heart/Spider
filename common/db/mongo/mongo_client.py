import time

import pymongo
from scrapy.conf import settings

from .mongo_constant import MongoConstant


class MongoClient(object):
    def __init__(self, db_name, collections_name):
        super(MongoClient, self).__init__()
        host_setting = settings[MongoConstant.MONGO_SERVER]
        port_setting = settings[MongoConstant.MONGO_PORT]

        self.__check_settings(host_setting, port_setting, db_name, collections_name)

        hosts = host_setting if isinstance(host_setting, list) else [host_setting]
        ports = port_setting if isinstance(port_setting, list) else [port_setting]

        address = []
        for host in hosts:
            for port in ports:
                address.append(str(host) + ':' + str(port))

        db = pymongo.MongoClient(address, readPreference='secondaryPreferred')[str(db_name)]

        user = settings[MongoConstant.MONGO_USER]
        password = settings[MongoConstant.MONGO_PASSWD]
        if user is not None and password is not None:
            db.authenticate(user, password)

        self.collections = {}
        if isinstance(collections_name, list) or isinstance(collections_name, tuple):
            for collection in collections_name:
                self.collections[collection] = db[collection]
        else:
            self.collections[collections_name] = db[collections_name]

        self.db = db

    def __check_settings(self, host, port, db, collection):
        if self.__check_var(host) and self.__check_var(port) and \
                self.__check_var(db) and self.__check_var(collection):
            return
        else:
            raise ValueError

    @classmethod
    def __check_var(cls, var):
        return False if var is None or '' else True

    def insert(self, collection, item):
        self.collections[collection].insert_one(item)

    def replace_one(self, collection, item, upsert=False, bypass_document_validation=False, collation=None):
        self.collections[collection].replace_one({'_id': item['_id']}, item, upsert,
                                                 bypass_document_validation, collation)

    @staticmethod
    def init_cname(task, market, country):
        search_collection_name = task + '_' + market + '_' + \
                                 country + '_' + str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))

        return search_collection_name
