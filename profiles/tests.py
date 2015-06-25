from django.test import SimpleTestCase, TestCase, RequestFactory
from django.core.urlresolvers import reverse
from .test_helpers import ProfileFactory, login_user, unverified_user, verified_user
from .views import ProfileDetail

class TestProfilePublicName(TestCase):
    def test_anonymous_name(self):
        p = ProfileFactory()
        self.assertEqual(p.name, 'Anonymous', 'Public name should be Anonymous if not set.')

    def test_displayed_public_name(self):
        p = ProfileFactory(public_name='foo')
        self.assertEqual(p.name, 'foo')

class TestProfileDetailPermissions(SimpleTestCase):
    def test_redirect_if_not_logged_in(self):
        path = reverse('profiles:detail')
        response = self.client.get(path, follow=True)
        expected = '{}?next={}'.format(reverse('account_login'), path)
        self.assertRedirects(response, expected)

    def test_verified_email_requirement(self):
        p = unverified_user()
        login_user(self.client, p)
        response = self.client.get(reverse('profiles:detail'))
        self.assertTemplateUsed(response, 'account/verified_email_required.html')
        self.assertTemplateNotUsed(response, 'profiles/profile_form.html')

class TestProfileDetailCanChange(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = verified_user()

    def test_verified_user_can_change_profile(self):
        request = self.factory.post(reverse('profiles:detail'), data={
            'profile_slug': 'foobar'
        })
        request.user = self.user
        response = ProfileDetail.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.user.profile_slug, 'foobar')
