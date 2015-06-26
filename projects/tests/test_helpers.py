import factory
from projects import models

class ProjectFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Project

    name            = factory.Sequence(lambda n: 'Project{}'.format(n))
    homepage        = factory.LazyAttribute(lambda p: 'http://{}.com'.format(p.name.lower().replace(' ', '')))
    code_of_conduct = factory.LazyAttribute(lambda p: '{}/code_of_conduct'.format(p.homepage))
