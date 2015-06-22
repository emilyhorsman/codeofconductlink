from django.forms import models
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Fieldset

def create_crispy_model_form(**form_kwargs):
    class BaseCrispyForm(models.ModelForm):
        def __init__(self, *args, **kwargs):
            super(BaseCrispyForm, self).__init__(*args, **kwargs)
            self.helper = FormHelper()
            self.helper.layout = Layout(
                Fieldset(form_kwargs.get('legend_text', ''), *self.Meta.fields),
                Submit('submit', form_kwargs.get('submit_text', 'Submit'), css_class='pure-button pure-button-primary')
            )
            self.helper.form_class = 'pure-form pure-form-stacked'
            self.helper.form_method = 'post'
            self.helper.form_action = form_kwargs.get('action', '')

    return BaseCrispyForm
