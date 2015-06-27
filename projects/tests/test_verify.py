from django.test import TestCase
from django.core.urlresolvers import reverse
from profiles.test_helpers import login_user, verified_user
from projects.models import Project, Submission
from .test_helpers import ProjectFactory, SubmissionFactory

class TestProjectVerification(TestCase):
    def setUp(self):
        self.admin = verified_user(is_staff=True)
        self.alice = verified_user()
        self.project = ProjectFactory(user=self.alice)
        self.verify_path = self.project.get_verify_url()

    def test_no_get_params(self):
        login_user(self.client, self.admin)
        response = self.client.post(reverse('projects:verify'))
        self.assertEqual(response.status_code, 404)

    def test_invalid_model_get_param(self):
        login_user(self.client, self.admin)
        response = self.client.post('{}?model=Foo'.format(reverse('projects:verify')))
        self.assertEqual(response.status_code, 404)

    def test_show_verify_button_to_moderator(self):
        login_user(self.client, self.admin)
        response = self.client.get(self.project.get_absolute_url())
        self.assertContains(response, self.verify_path)

    def test_hide_verify_button_from_others(self):
        login_user(self.client, self.alice)
        response = self.client.get(self.project.get_absolute_url())
        self.assertNotContains(response, self.verify_path)

    def test_verify_permissions(self):
        response = self.client.post(self.verify_path)
        self.assertEqual(response.status_code, 302)
        login_user(self.client, self.alice)
        response = self.client.post(self.verify_path)
        self.assertEqual(response.status_code, 302)

    def test_toggle_verification(self):
        login_user(self.client, self.admin)
        response = self.client.post(self.verify_path)
        p = Project.objects.get(pk=self.project.pk)
        self.assertTrue(response['Location'].endswith(self.project.get_absolute_url()))
        self.assertTrue(p.verified_date > p.created_date)
        self.assertEqual(p.verified_by, self.admin)

        response = self.client.post(self.verify_path)
        p = Project.objects.get(pk=self.project.pk)
        self.assertTrue(response['Location'].endswith(self.project.get_absolute_url()))
        self.assertFalse(p.verified_date)
        self.assertFalse(p.verified_by)

class TestSubmissionVerification(TestCase):
    def setUp(self):
        self.admin = verified_user(is_staff=True)
        self.alice = verified_user()
        self.project = ProjectFactory(user=self.alice)
        self.project.toggle_verify(self.admin)
        self.submission = SubmissionFactory(user=self.alice, project=self.project)
        self.verify_path = self.submission.get_verify_url()

    def test_toggle_verification(self):
        login_user(self.client, self.admin)
        response = self.client.post(self.verify_path)
        s = Submission.objects.get(pk=self.submission.pk)
        self.assertTrue(response['Location'].endswith(self.project.get_absolute_url()))
        self.assertTrue(s.verified_date > s.created_date)
        self.assertEqual(s.verified_by, self.admin)

        response = self.client.post(self.verify_path)
        s = Submission.objects.get(pk=self.submission.pk)
        self.assertTrue(response['Location'].endswith(self.project.get_absolute_url()))
        self.assertFalse(s.verified_date)
        self.assertFalse(s.verified_by)
