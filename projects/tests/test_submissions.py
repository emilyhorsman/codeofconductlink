from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import AnonymousUser
from profiles.test_helpers import login_user, verified_user
from .test_helpers import ProjectFactory, SubmissionFactory

class TestViewSubmissionsInProject(TestCase):
    def setUp(self):
        self.admin   = verified_user(is_staff=True)
        self.alice   = verified_user()
        self.ada     = verified_user()
        self.project = ProjectFactory(user=self.alice)
        self.project.toggle_verify(self.admin)

        self.uv_alice_submission = SubmissionFactory(user=self.alice, project=self.project)
        self.v_alice_submission  = SubmissionFactory(user=self.alice, project=self.project)
        self.uv_ada_submission   = SubmissionFactory(user=self.ada, project=self.project)
        self.v_ada_submission    = SubmissionFactory(user=self.ada, project=self.project)
        self.v_alice_submission.toggle_verify(self.admin)
        self.v_ada_submission.toggle_verify(self.admin)

    def test_get_submissions_admin(self):
        submissions = self.project.get_submissions_for_user(self.admin)
        self.assertTrue(self.v_alice_submission in submissions)
        self.assertTrue(self.v_ada_submission in submissions)
        self.assertTrue(self.uv_alice_submission in submissions)
        self.assertTrue(self.uv_ada_submission in submissions)

    def test_get_submissions_no_user(self):
        submissions = self.project.get_submissions_for_user(AnonymousUser())
        self.assertTrue(self.v_alice_submission in submissions)
        self.assertTrue(self.v_ada_submission in submissions)
        self.assertFalse(self.uv_alice_submission in submissions)
        self.assertFalse(self.uv_ada_submission in submissions)

    def test_get_submissions_for_alice(self):
        submissions = self.project.get_submissions_for_user(self.alice)
        self.assertTrue(self.v_alice_submission in submissions)
        self.assertTrue(self.v_ada_submission in submissions)
        self.assertTrue(self.uv_alice_submission in submissions)
        self.assertFalse(self.uv_ada_submission in submissions)

    def test_no_user_views_only_verified_submission(self):
        response = self.client.get(self.project.get_absolute_url())
        self.assertContains(response, self.v_alice_submission.url)
        self.assertContains(response, self.v_ada_submission.url)
        self.assertNotContains(response, self.uv_alice_submission.url)
        self.assertNotContains(response, self.uv_ada_submission.url)

    def test_admin_views_all_submissions(self):
        login_user(self.client, self.admin)
        response = self.client.get(self.project.get_absolute_url())
        self.assertContains(response, self.v_alice_submission.url)
        self.assertContains(response, self.v_ada_submission.url)
        self.assertContains(response, self.uv_alice_submission.url)
        self.assertContains(response, self.uv_ada_submission.url)

    def test_alice_views_verified_submissions_and_hers(self):
        login_user(self.client, self.alice)
        response = self.client.get(self.project.get_absolute_url())
        self.assertContains(response, self.v_alice_submission.url)
        self.assertContains(response, self.v_ada_submission.url)
        self.assertContains(response, self.uv_alice_submission.url)
        self.assertNotContains(response, self.uv_ada_submission.url)

class TestCreateProjectSubmission(TestCase):
    def setUp(self):
        self.admin = verified_user(is_staff=True)
        self.alice = verified_user()
        self.project = ProjectFactory(user=self.alice)
        self.project.toggle_verify(self.admin)
