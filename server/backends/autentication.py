from server.bom.user import *
from server.mongodb.driver import *

import logging
logger = logging.getLogger("echaloasuerte")

class EchaloasuerteAuthBE(object):
    """
    Authenticate against echaloasuerte users
    """

    def authenticate(self, username=None, password=None):
        logger.debug("Autenticating username: {0}".format(username))
        try:
            MongoDriver.instance().retrieve_user(User,username)
            if user.check_password(password):
                logger.debug("Success")
                return user
        except Exception as e:
            logger.info("Exception when autenticating {0}: {1}".format(username,e))
        logger.debug("Failed")
        return None

    def get_user(self, user_id):
        try:
            return MongoDriver.instance().retrieve_user(User,username)
        except User.DoesNotExist:
            return None
