from django.forms import models
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Fieldset

def pure_helper(**kwargs):
    helper = FormHelper()
    helper.form_class  = kwargs.get('class', 'pure-form pure-form-stacked')
    helper.form_method = kwargs.get('method', 'post')
    helper.form_action = kwargs.get('action', '')
    helper.field_tempalte = 'uni_form/field.html'
    return helper

def create_crispy_model_form(**form_kwargs):
    class BaseCrispyForm(models.ModelForm):
        def __init__(self, *args, **kwargs):
            super(BaseCrispyForm, self).__init__(*args, **kwargs)
            self.helper = pure_helper()
            self.helper.layout = Layout(
                Fieldset(form_kwargs.get('legend_text', ''), *self.Meta.fields),
                Submit('submit', form_kwargs.get('submit_text', 'Submit'), css_class='pure-button pure-button-primary')
            )

    return BaseCrispyForm
