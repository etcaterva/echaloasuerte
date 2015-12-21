import logging

from django.core.exceptions import PermissionDenied
from django.http.response import HttpResponseForbidden


logger = logging.getLogger("echaloasuerte")
from server.mongodb.driver import MongoDriver
from django.views.defaults import page_not_found


class ExceptionMiddleware(object):
    """
    Middleware to handle custom project exceptions
    """

    def __init__(self):
        pass

    def process_exception(self, request, exception):
        logger.info("Processing unhandled exception {0}".format(exception))
        if isinstance(exception, MongoDriver.NotFoundError):
            return page_not_found(request)

        if isinstance(exception, MongoDriver.DecodingError):
            logger.error("Unexpected Exception, returning not found. {0}".format(exception))
            return page_not_found(request)

        if isinstance(exception, PermissionDenied):
            return HttpResponseForbidden()

        logger.info("Exception not handled, propagating...")
        logger.exception(exception)

