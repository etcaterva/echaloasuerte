import pymongo
import logging
logger = logging.getLogger("echaloasuerte")
from server.bom.coin import *
from server.bom.dice import *
from server.bom.random_number import *
from server.bom.card import *
from server.bom.link_sets import *
from server.bom.random_item import *
from server.bom.user import User
from bson.objectid import ObjectId

import datetime
import pytz

def safe_connection(func):
    """decorator to restart the connection if needed"""
    def _(*args,**kwargs):
        try:
            return func(*args,**kwargs)
        except (pymongo.errors.AutoReconnect, pymongo.errors.ConnectionFailure) as e:
            logger.error("PymongoError: {0} resetting mongo connection... ".format(e))
            MongoDriver._instance = None
    return _

def build_draw(doc):
    """Given a python dict that represnets a draw, builds it"""
    try:
        return eval(doc["draw_type"])(**doc)
    except Exception as e:
        logger.error("Error when decoding a draw. Exception: {1}. Draw: {0} ".format(doc,e))
        raise

class MongoDriver(object):
    """
    Singleton to handle access to mongodb
    """

    class MongoException(Exception):
        """
        MongoDB Exception
        """
        pass

    class NotFoundError(MongoException):
        """
        Exception thrown whenever an object is not found in mongo
        """
        pass


    class DecodingError(MongoException):
        """
        Exception thrown whenever the decoding of an object fails
        """
        pass

    _instance = None
    def __init__(self, host='localhost', port=27017, database='echaloasuerte'):
        self.client = pymongo.MongoClient(host,port)
        self._db = self.client[database]
        self._users = self._db.users
        self._draws = self._db.draws
        self._chats = self._db.chats


    @safe_connection
    def create_user(self,user):
        if self._users.find({"_id":user._id}).count() == 0:
            self.save_user(user)
        else:
            logger.debug("User {0} already exists".format(user._id))
            raise Exception("User already exists")

    @safe_connection
    def save_user(self,user):
        """Given a user, saves it, returns the _id"""
        doc = user.__dict__
        self._users.save(doc)
        logger.debug("Saved documment: {0}".format(doc))
        return doc["_id"]

    @safe_connection
    def retrieve_user(self,user_id):
        doc = self._users.find_one({"_id":user_id})
        if doc is None:
            raise MongoDriver.NotFoundError("User not found: {0}".format(user_id))
        logger.debug("Retrieved documment: {0} using id {1}".format(doc,user_id))
        return User(**doc)

    @safe_connection
    def get_draws_with_filter(self, d_filter, num_results = 100):
        res_draws = [build_draw(x) for x in self._draws.find(d_filter).sort("creation_time",pymongo.DESCENDING).limit(num_results)]
        res_draws = [x for x in res_draws if x is not None]
        logger.debug("Found {0} draws with filter {1}".format(len(res_draws ),d_filter))
        return res_draws

    @safe_connection
    def get_user_draws(self, user_id, num_results = 50):
        owner_draws = [build_draw(x) for x in self._draws.find({"owner":user_id}).sort("creation_time",pymongo.DESCENDING).limit(num_results)]
        owner_draws = [x for x in owner_draws if x is not None]
        #todo: related
        logger.debug("Found {0} draws of which {1} is owner".format(len(owner_draws),user_id))
        return {"user_id":user_id,"owner":owner_draws}

    @safe_connection
    def save_draw(self,draw):
        """Given a draw, saves it, update its ID if not set and returns the _id"""
        doc = draw.__dict__
        if "_id" in doc.keys() and doc["_id"] is None:#Ask mongo to generate an id
            doc.pop("_id")
        self._draws.save(doc)
        draw._id = doc["_id"]
        logger.debug("Saved documment: {0}".format(doc))
        return doc["_id"]

    @safe_connection
    def retrieve_draw(self,draw_id):
        """
        Retrieves a draw from mongo.
        Get the type from the serialized object
        """
        try:
            raw_id = ObjectId(draw_id) if draw_id is not ObjectId else draw_id
        except:
            raise MongoDriver.NotFoundError("Error with id: {0}".format(draw_id))
        doc = self._draws.find_one({"_id":raw_id})
        if doc is None:
            raise MongoDriver.NotFoundError("Draw not found: {0}".format(draw_id))
        logger.debug("Retrieved documment: {0}".format(doc))
        return build_draw(doc)

    def add_chat_message(self, draw_id, content, user_name):
        """ add a mesago to a chat. we'll use draw id as chat-id"""
        now = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)
        entry = {
            "user" : user_name,
            "content" : content,
            "creation_time" : now
        }
        self._chats.update(
                { "_id" : draw_id },
                { "$push" : { "entries" : entry } },
                upsert = True
        )

    def retrieve_chat_messages(self, draw_id):
        """ retrieves all messages of a chat given its chat id (draw id)"""
        logger.debug("Retrieving chat with id {0}".format(draw_id))
        doc = self._chats.find_one( { "_id" : draw_id } )
        if doc is None:
            raise MongoDriver.NotFoundError("Chat not found: {0}".format(draw_id))
        entries = doc["entries"]
        logger.debug("Retrieved documment chat {0} with {1} entries "
                .format(draw_id, len(entries)))
        return sorted ( entries, key=lambda k: k['creation_time'], reverse = True)

    @staticmethod
    def instance():
        if MongoDriver._instance is None:
            from django.conf import settings
            for cnx_param in settings.MONGO_END_POINTS:
                try:
                    MongoDriver._instance = MongoDriver(**cnx_param)
                except Exception as e:
                    logger.warning("Imposible to connect to mongo DB using parameters {0}, exception: {1}".format(cnx_param,e))
                else:
                    logger.info("Connected to to mongo using parameter {0}".format(cnx_param))

                if MongoDriver._instance: break

        assert(MongoDriver._instance is not None)
        return MongoDriver._instance

