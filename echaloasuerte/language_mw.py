from django.utils import translation
import six

LANGUAGE_DOMAINS = {
    'es': 'echaloasuerte.com',
    'en': 'chooserandom.com',
    'en': 'pickforme.net',
}


class LangInDomainMiddleware(object):
    """
    Middleware for determining site's language via the domain name used in
    the request.
    This needs to be installed after the LocaleMiddleware so it can override
    that middleware's decisions.
    """

    def process_request(self, request):
        lang_selected = 'es' # Default to spanish (only if domain not found)
        for lang, lang_domain in six.iteritems(LANGUAGE_DOMAINS.iteritems()):
            host = request.META.get('HTTP_HOST')
            if host == None:
                break
            if (lang_domain in host):
                lang_selected = lang
                break

        translation.activate(lang_selected)
        request.LANGUAGE_CODE = translation.get_language()
