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
        fields = ('resolved', 'message',)

    # The message should be readonly if the user is not the owner. (e.g.
    # moderator is resolving a report)
    # http://stackoverflow.com/questions/324477/in-a-django-form-how-to-make-a-field-readonly-or-disabled-so-that-it-cannot-b
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('request_user')
        super(UpdateReportForm, self).__init__(*args, **kwargs)
        if user.is_moderator:
            self.instance.message_readonly = True
            self.fields['message'].widget = TextWidget()
            self.fields['message'].widget.attrs['readonly'] = True

    def clean_message(self):
        # We don't care what the moderator has to say. Return the original
        # message (it is readonly to moderators).
        if getattr(self.instance, 'message_readonly', False):
            del self.instance.message_readonly
            return self.instance.message
        return self.cleaned_data['message']
