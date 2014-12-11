from pymongo import MongoClient

class MongoDriver(object):
    _instance = None
    def __init__(self, host='localhost', port=27017, database='echaloasuerte'):
        self.client = MongoClient(host,port)
        self._db = self.client[database]
        self._users = self._db.users
        self._draws = self._db.draws


    def save_draw(self,draw):
        """Given a draw, saves it, update its ID if not set and returns the _id"""
        doc = draw.__dict__
        if doc["_id"] is None:#Ask mongo to generate an id
            doc.pop("_id")
        self._draws.save(doc)
        draw._id = doc["_id"]
        return doc["_id"]

    def retrieve_draw(self,draw_class,draw_id):
        """
        Retrieves a draw from mongo. given its class and its id
        E.g.: retrieve_draw(RandomNumberDraw,"dsdfdsafdsa")
        It returns an object of type draw_class
        """
        doc = self._draws.find_one({"_id":draw_id})
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


