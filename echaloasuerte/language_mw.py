from django.utils import translation

LANGUAGE_DOMAINS = {
    'echaloasuerte': 'es',
    'chooserandom': 'en',
}
DEFAULT_LANGUAGE = 'es'


class LangInDomainMiddleware(object):
    """
    Middleware for determining site's language via the domain name used in
    the request.
    This needs to be installed after the LocaleMiddleware so it can override
    that middleware's decisions.
    """

    def process_request(self, request):
        host = request.META.get('HTTP_HOST', '')
        host_domain = [_ for _ in host.split('.') if _ in LANGUAGE_DOMAINS]
        if host_domain:
            language = LANGUAGE_DOMAINS[host_domain[0]]
        else:
            language = DEFAULT_LANGUAGE
        translation.activate(language)
        request.LANGUAGE_CODE = translation.get_language()
