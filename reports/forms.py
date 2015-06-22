from django.forms import models, Widget
from .models import Report

class UpdateReportForm(models.ModelForm):
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
            self.fields['message'].widget.attrs['readonly'] = True

    def clean_message(self):
        return self.instance.message
