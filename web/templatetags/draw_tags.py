from django.core.urlresolvers import reverse
from django import template

register = template.Library()


@register.filter
def permalink(draw_bom, request):
    return request.META['HTTP_HOST'] + reverse('retrieve_draw', args=[draw_bom.pk])
