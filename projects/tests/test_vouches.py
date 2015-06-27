from django.test import TestCase
from django.utils.http import urlquote
from django.core.urlresolvers import reverse
from profiles.test_helpers import login_user, verified_user
from projects.models import Vouch
from .test_helpers import ProjectFactory

class TestProjectVouch(TestCase):
    def setUp(self):
        self.admin = verified_user(is_staff=True)
        self.alice = verified_user()
        self.project = ProjectFactory(user=self.alice, name='Foo')
        self.project.toggle_verify(self.admin)
        self.vouch_path = '{path}?model={model}&pk={pk}'.format(path=reverse('projects:vouch'),
                                                               model=self.project.__class__.__name__,
                                                               pk=self.project.pk)

    def test_vouch_redirects_if_not_logged_in(self):
        response = self.client.post(self.vouch_path)
        self.assertEqual(response.status_code, 302)

    def test_no_get_params(self):
        login_user(self.client, self.alice)
        response = self.client.post(reverse('projects:vouch'))
        self.assertEqual(response.status_code, 404)

    def test_invalid_model_get_param(self):
        login_user(self.client, self.alice)
        response = self.client.post('{path}?model=Foo'.format(path=reverse('projects:vouch')))
        self.assertEqual(response.status_code, 404)

    def test_invalid_pk_get_param(self):
        login_user(self.client, self.alice)
        response = self.client.post(self.vouch_path + "99999")
        self.assertEqual(response.status_code, 404)

    def test_vouch_toggle(self):
        login_user(self.client, self.alice)
        response = self.client.post(self.vouch_path, follow=True)
        self.assertRedirects(response, self.project.get_absolute_url())
        self.assertTrue(self.project.vouches.filter(user=self.alice).exists())

        response = self.client.post(self.vouch_path, follow=True)
        self.assertRedirects(response, self.project.get_absolute_url())
        self.assertFalse(self.project.vouches.filter(user=self.alice).exists())
