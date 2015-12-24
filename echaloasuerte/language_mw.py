from django.utils import translation

LANGUAGE_DOMAINS = {
    'es': 'echaloasuerte.com',
    'en': 'chooserandom.com',
}


class LangInDomainMiddleware(object):
    """
    Middleware for determining site's language via the domain name used in
    the request.
    This needs to be installed after the LocaleMiddleware so it can override
    that middleware's decisions.
    """

    def process_request(self, request):
        for lang in LANGUAGE_DOMAINS.keys():
            lang_domain = LANGUAGE_DOMAINS[lang]
            servername = request.META.get('SERVER_NAME')
            host = request.META.get('HTTP_HOST')
            if (servername and lang_domain in servername
                or host and lang_domain in host):
                translation.activate(lang)
                request.LANGUAGE_CODE = translation.get_language()
