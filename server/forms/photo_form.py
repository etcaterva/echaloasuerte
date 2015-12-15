from django import forms
from django.utils.translation import ugettext_lazy as _
from crispy_forms.layout import Layout, Row, HTML

from server.forms import FormBase


class PhotoDrawForm(FormBase):
    number_of_results = forms.IntegerField(label=_("Number of points"),
                                           required=True, initial=1)
    photo_url = forms.URLField(label=_("Photo URL"),
                                required=True)

    DEFAULT_TITLE = _("Photo Draw")

    def __init__(self, *args, **kwargs):
        super(PhotoDrawForm, self).__init__(*args, **kwargs)

        # Add "protected" class to the input that will be read-only when the
        # draw is public
        self.fields['number_of_results'].widget.attrs.update(
            {'class': 'protected', 'min': 1})

        self.helper.label_class = 'col-xs-6 text-right'
        self.helper.field_class = 'col-xs-6'
        self.helper.layout = Layout(
            Row(
                Row('number_of_results'),
                'photo_url',
            ),
            Row(
                HTML("""<canvas id="canvas-main" width="0" height="0" data-url="{{bom.photo_url}}" data-points="{% with bom.results|last as results%}{%for result in results.items%}{{result|join:","}}{%endfor%}{%endwith%}"></canvas>"""
                    """<script>draw_canvas($("#canvas-main"));</script>""", )
            )
        )
