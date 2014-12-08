from pymongo import MongoClient


class MongoDriver(object):
    def __init__(self, host='localhost', port=27017, database='echaloasuerte'):
        self.client = MongoClient(host,port)
        self._db = self.client[database]
        self._users = self._db.users
        self._draws = self._db.draws
