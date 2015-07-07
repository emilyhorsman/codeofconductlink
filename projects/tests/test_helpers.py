import factory
from projects import models

class ProjectFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Project

    name            = factory.Sequence(lambda n: 'Project{}'.format(n))
    homepage        = factory.LazyAttribute(lambda p: 'http://{}.com'.format(p.name.lower().replace(' ', '')))
    code_of_conduct = factory.LazyAttribute(lambda p: '{}/code_of_conduct'.format(p.homepage))

class SubmissionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Submission

    url = factory.Sequence(lambda n: 'http://test.com/contributors/{}'.format(n))
    is_contributor = True
    public_message = factory.Sequence(lambda n: 'They are contributor #{} to this project.'.format(n))
    private_message = factory.Sequence(lambda n: 'You can contact contributor #{n} at contributor{n}@test.com'.format(n=n))

def make_project(test, project_user, verify_user=None):
    p = ProjectFactory(user=project_user)
    if verify_user:
        p.toggle_verify(verify_user)
    return p

def make_submission_on_project(test, user, verify_user=None):
    s = SubmissionFactory(user=user, project=test.project)
    if verify_user:
        s.toggle_verify(verify_user)
    return s
