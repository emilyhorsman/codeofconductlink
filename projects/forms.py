from django.forms import models
from crispy_forms.layout import Submit, Layout, Fieldset, Field
from common.forms import pure_helper, create_crispy_model_form
from profiles.recaptcha import ReCAPTCHAField
from .models import Project, Report, Submission

class CreateProjectForm(models.ModelForm):
    class Meta:
        model = Project
        fields = ('name', 'homepage', 'code_of_conduct', 'tags',)

    recaptcha = ReCAPTCHAField(label='')

    def __init__(self, *args, **kwargs):
        super(CreateProjectForm, self).__init__(*args, **kwargs)
        self.helper = pure_helper()
        self.helper.layout = Layout(
            Fieldset('Submit a new project for tracking', 'recaptcha', *self.Meta.fields),
            Submit('submit', 'Create', css_class='pure-button pure-button-primary')
        )


class UpdateProjectForm(create_crispy_model_form(
                        legend_text='Edit Project')):
    class Meta:
        model = Project
        fields = ('name', 'homepage', 'code_of_conduct', 'tags',)


class CreateSubmissionForm(models.ModelForm):

    class Meta:
        model = Submission
        fields = ('url', 'tags', 'is_contributor', 'public_message', 'private_message',)
        labels = {
            'url': 'URL',
        }

    def __init__(self, *args, **kwargs):
        project = kwargs.pop('project')
        super(CreateSubmissionForm, self).__init__(*args, **kwargs)

        self.fields['url'].widget.attrs['placeholder'] = 'https://somecontributorhomepage.alice'
        self.fields['tags'].widget.attrs['placeholder'] = 'queer, contributor'
        self.fields['public_message'].widget.attrs.update({
            'placeholder': 'Alice identifies as queer and is a core contributor to codeofconduct.',
            'rows': 2
        })
        self.fields['private_message'].widget.attrs.update({
            'placeholder': 'You can reach them at me@somecontributorhomepage.alice',
            'rows': 2
        })

        self.helper = pure_helper()
        self.helper.layout = Layout(
            Fieldset('Creating a submission for {}'.format(project),
                     *self.Meta.fields),
            Submit('submit', 'Create', css_class='pure-button pure-button-primary')
        )
