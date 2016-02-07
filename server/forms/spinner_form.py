from django.templatetags.static import static
from django.utils.translation import ugettext_lazy as _
from crispy_forms.layout import Layout, HTML

from server.forms.form_base import FormBase


class SpinnerDrawForm(FormBase):
    DEFAULT_TITLE = _("Spinner")

    def __init__(self, *args, **kwargs):
        super(SpinnerDrawForm, self).__init__(*args, **kwargs)
        self.helper.layout = Layout(
            HTML(
                '<div class="text-center">'
                '<a href="#">'
                '<img type="image" id="img-spinner" src="{0}" width="70%" name="spinner" '
                '''onclick="$('#create-and-toss,#normal-draw-toss, #shared-draw-toss, #try').click();" />'''
                '</a><p>{1}</p></div>'.format(
                    static('img/draw_icons/spinner.svg'), _("Tap the spinner to spin it")))
        )
