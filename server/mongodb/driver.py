from pymongo import MongoClient
import logging
logger = logging.getLogger("echaloasuerte")

class MongoDriver(object):
    _instance = None
    def __init__(self, host='localhost', port=27017, database='echaloasuerte'):
        self.client = MongoClient(host,port)
        self._db = self.client[database]
        self._users = self._db.users
        self._draws = self._db.draws
        logger.info("Connected to '{0}' port '{1}' database '{2}'".format(host,port,database))

    def save_user(self,user):
        """Given a user, saves it, update its ID if not set and returns the _id"""
        doc = user.__dict__
        if "_id" in doc.keys() and doc["_id"] is None:#Ask mongo to generate an id
            doc.pop("_id")
        self._users.save(doc)
        user._id = doc["_id"]
        logger.debug("Saved documment: {0}".format(doc))
        return doc["_id"]

    def retrieve_user(self,user_type,user_id):
        doc = self._users.find_one({"_id":user_id})
        logger.debug("Retrieved documment: {0}".format(doc))
        return user_type(**doc)

    def retrieve_user_by_email(self,user_type,email):
        doc = self._users.find_one({"email":email})
        logger.debug("Retrieved documment: {0}".format(doc))
        return user_type(**doc)

    def save_draw(self,draw):
        """Given a draw, saves it, update its ID if not set and returns the _id"""
        doc = draw.__dict__
        if "_id" in doc.keys() and doc["_id"] is None:#Ask mongo to generate an id
            doc.pop("_id")
        self._draws.save(doc)
        draw._id = doc["_id"]
        logger.debug("Saved documment: {0}".format(doc))
        return doc["_id"]

    def retrieve_draw(self,draw_class,draw_id):
        """
        Retrieves a draw from mongo. given its class and its id
        E.g.: retrieve_draw(RandomNumberDraw,"dsdfdsafdsa")
        It returns an object of type draw_class
        """
        doc = self._draws.find_one({"_id":draw_id})
        logger.debug("Retrieved documment: {0}".format(doc))
        return draw_class(**doc)

    @staticmethod
    def instance():
        try:
            if MongoDriver._instance is None:
                from django.conf import settings
                cnx_param = settings.MONGO_HOST,settings.MONGO_PORT,settings.MONGO_DB
                MongoDriver._instance = MongoDriver(*cnx_param)
            return MongoDriver._instance
        except Exception as e:
            print( "Imposible to connect to mongo db: {0}".format(e))


