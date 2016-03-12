from django import forms
from django.utils.translation import ugettext_lazy as _, ugettext
from crispy_forms.layout import Layout, Row, HTML, Field

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
        self.fields['number_of_results'].widget.attrs.update({'class': 'protected', 'min': 1})
        self.fields['photo_url'].widget.attrs.update({'class': 'protected'})

        self.helper.label_class = 'col-xs-6 text-right'
        self.helper.field_class = 'col-xs-6'
        self.helper.layout = Layout(
            Row(
                Row('number_of_results'),
                Field('photo_url', wrapper_class="protected-hidden clearfix"),
                HTML('<div class="text-center"><button type="button" id="fetch-fb-photos" class="btn btn-social hidden protected protected-hidden btn-facebook"><span class="fa fa-facebook"></span>{0}</button></div>'.format(ugettext('Use a picture from Facebook')))
            ),
            Row(
                HTML("""<canvas id="canvas-photo-main" width="0" height="0" data-url="{{bom.photo_url}}" data-points="{% with bom.results|last as results%}{%for result in results.items%}{{result|join:","}}{%endfor%}{%endwith%}"></canvas>"""
                    """<script>draw_canvas($("#canvas-photo-main"));</script>""", )
            )
        )
