from django.templatetags.static import static
from django.utils.translation import ugettext_lazy as _
from crispy_forms.layout import Layout, HTML

from server.forms.form_base import FormBase


class CoinDrawForm(FormBase):
    DEFAULT_TITLE = _("Flip a Coin")

    def __init__(self, *args, **kwargs):
        super(CoinDrawForm, self).__init__(*args, **kwargs)

        self.helper.layout = Layout(
            HTML(
                '<div class="text-center">'
                '<a href="#">'
                '<img type="image" id="img-coin" src="{0}" name="coin" '
                '''onclick="$('#create-and-toss,#normal-draw-toss, #shared-draw-toss, #try').click();" />'''
                '<a>'
                '<p>{1}</p></div>'.format(
                    static('img/img_coin/head.png'), _("Tap the coin to flip it")))
        )
