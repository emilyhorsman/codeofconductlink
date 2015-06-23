from django.forms import models, Widget
from crispy_forms.layout import Submit, Layout, Fieldset, HTML
from common.forms import pure_helper, create_crispy_model_form
from .models import Report

class TextWidget(Widget):
    def render(self, name, value, attrs=None):
        return '<p>{}</p>'.format(value)

class CreateReportForm(models.ModelForm):
    class Meta:
        model  = Report
        fields = ('message', 'visible_to_owner',)

    def __init__(self, *args, **kwargs):
        target = kwargs.pop('target')
        super(CreateReportForm, self).__init__(*args, **kwargs)
        self.helper = pure_helper()
        self.helper.layout = Layout(
            Fieldset('Filing a report on {}'.format(target),
                     HTML("""<p class="backed form-message">Your report will only be visible to moderators by default. It will never be available to the general public.</p>"""),
                     *self.Meta.fields),
            Submit('submit', 'File Report', css_class='pure-button pure-button-primary')
        )

class UpdateReportForm(create_crispy_model_form(legend_text='Modify report resolution')):
    class Meta:
        model  = Report
        fields = ('resolved', 'visible_to_owner', 'message',)

    # The message should be readonly if the user is not the owner. (e.g.
    # moderator is resolving a report)
    # http://stackoverflow.com/questions/324477/in-a-django-form-how-to-make-a-field-readonly-or-disabled-so-that-it-cannot-b
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('request_user')
        super(UpdateReportForm, self).__init__(*args, **kwargs)
        # Moderators can't edit _other_ people's messages.
        if user.is_moderator and self.instance.user != user:
            self.instance.only_edit_resolution = True
            self.fields['message'].widget = TextWidget()
            self.fields['message'].widget.attrs['readonly'] = True
            self.fields['visible_to_owner'].widget = TextWidget()
            self.fields['visible_to_owner'].widget.attrs['readonly'] = True

    def clean(self):
        # We don't care what the moderator has to say. Return the original
        # fields that don't involve report resolution.
        if getattr(self.instance, 'only_edit_resolution', False):
            del self.instance.only_edit_resolution
            self.cleaned_data['message'] = self.instance.message
            self.cleaned_data['visible_to_owner'] = self.instance.visible_to_owner
