from django.test import SimpleTestCase
from django.core.urlresolvers import reverse
from profiles.test_helpers import ProfileFactory, login_user, unverified_user, verified_user

class TestCreateProjectPermissions(SimpleTestCase):
    def test_login_requirement(self):
        path = reverse('projects:create')
        response = self.client.get(path, follow=True)
        expected = '{}?next={}'.format(reverse('account_login'), path)
        self.assertRedirects(response, expected)

    def test_verified_email_requirement(self):
        p = unverified_user()
        login_user(self.client, p)
        response = self.client.get(reverse('projects:create'))
        self.assertTemplateUsed(response, 'account/verified_email_required.html')
        self.assertTemplateNotUsed(response, 'projects/project_form.html')

    def test_verified_user_shows_form(self):
        p = verified_user()
        login_user(self.client, p)
        response = self.client.get(reverse('projects:create'))
        self.assertTemplateUsed(response, 'projects/project_form.html')
