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
