from crispy_forms.layout import Layout
from server.forms.form_base import FormBase


class CoinDrawForm(FormBase):

    def __init__(self, *args, **kwargs):
        super(CoinDrawForm, self).__init__(*args, **kwargs)

        self.helper.layout = Layout(
            None,  # Keep it empty, since we don't want to render the title
        )
