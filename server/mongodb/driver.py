from pymongo import MongoClient

class MongoDriver(object):
    _instance = None
    def __init__(self, host='localhost', port=27017, database='echaloasuerte'):
        self.client = MongoClient(host,port)
        self._db = self.client[database]
        self._users = self._db.users
        self._draws = self._db.draws

    @staticmethod
    def instance():
        try:
            if MongoDriver._instance is None:
                from django.conf import settings
                cnx_param = settings.MONGO_HOST,settings.MONGO_PORT,settings.MONGO_DB
                MongoDriver._instance = MongoDriver(*cnx_param)
            return MongoDriver._instance
        except Exception as e:
            print "Imposible to connect to mongo db. ".format(e)


