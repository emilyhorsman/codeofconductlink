from allauth.account.models import EmailAddress
import factory
from . import models

class ProfileFactory(factory.Factory):
    class Meta:
        model = models.Profile

    email = factory.Sequence(lambda n: 'test{}@example.com'.format(n))

def login_user(client, user):
    client.login(email=user.email, password='testing')

def unverified_user(**kwargs):
    p = ProfileFactory(**kwargs)
    p.set_password('testing')
    p.save()
    return p

def verified_user(**kwargs):
    p = unverified_user(**kwargs)
    e = EmailAddress(user=p, verified=True)
    e.save()
    return p
