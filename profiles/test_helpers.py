from django.test import TestCase
from django.core.urlresolvers import reverse
from allauth.account.models import EmailAddress
import factory
from . import models

class ProfileFactory(factory.django.DjangoModelFactory):
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
    e = EmailAddress(user=p, email=p.email, verified=True)
    e.save()
    return p

def test_login_redirect(test, protected_path):
    response = test.client.get(protected_path, follow=True)
    expected = '{}?next={}'.format(reverse('account_login'), protected_path)
    test.assertRedirects(response, expected)

def test_verified_email_requirement(test, **protected):
    p = unverified_user()
    login_user(test.client, p)
    response = test.client.get(protected['path'])
    test.assertTemplateUsed(response, 'account/verified_email_required.html')
    if 'template' in protected:
        test.assertTemplateNotUsed(response, protected['template'])
