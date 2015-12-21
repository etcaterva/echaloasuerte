import logging

from server.mongodb.driver import *


logger = logging.getLogger("echaloasuerte")


class EchaloasuerteAuthBE(object):
    """
    Authenticate against echaloasuerte users
    """

    def authenticate(self, username=None, password=None):
        logger.debug("Autenticating username: {0}".format(username))
        try:
            user = MongoDriver.instance().retrieve_user(username)
            if user.check_password(password):
                logger.debug("Success")
                return user
        except Exception as e:
            logger.info("Exception when autenticating {0}: {1}".format(username, e))
        logger.debug("Failed")
        return None

    def get_user(self, user_id):
        try:
            return MongoDriver.instance().retrieve_user(user_id)
        except Exception as e:
            logger.debug("When retrieving user {0}, Exception: {1}".format(user_id, e))
            return None
