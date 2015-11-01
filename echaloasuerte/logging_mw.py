import logging

LOG = logging.getLogger('echaloasuerte.access')


class RequestLoggerMiddleware(object):
    def process_request(self, request):
        LOG.debug(
            "User '{0}' requests '{1}' with GET: {2} and POST: {3}".format(
                request.user, request.path, request.GET, request.POST
            ))
        return None

