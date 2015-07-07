from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import AnonymousUser
from profiles.test_helpers import login_user, verified_user
from .test_helpers import ProjectFactory, SubmissionFactory
from . import test_helpers
import profiles.test_helpers

class TestViewSubmissionsInProject(TestCase):
    def setUp(self):
        profiles.test_helpers.setup_alice_and_ada_test(self)
        self.project = test_helpers.make_project(self.alice, self.admin)
        self.submissions = [
            test_helpers.make_submission_on_project(self, self.alice, self.admin),
            test_helpers.make_submission_on_project(self, self.alice),
            test_helpers.make_submission_on_project(self, self.ada, self.admin),
            test_helpers.make_submission_on_project(self, self.ada),
        ]

    def test_get_submissions_admin(self):
        project_submissions = self.project.get_submissions_for_user(self.admin)
        self.assertTrue(
            all(s in project_submissions for s in self.submissions),
            'Not all submissions appeared for the admin.'
        )

    def test_get_submissions_no_user(self):
        project_submissions = self.project.get_submissions_for_user(AnonymousUser())
        for s in self.submissions:
            self.assertEqual(
                s in project_submissions,
                s.is_verified(),
                'Anonymous user should only see verified submissions.'
            )

    def test_get_submissions_for_alice(self):
        project_submissions = self.project.get_submissions_for_user(self.alice)
        for s in self.submissions:
            self.assertEqual(
                s in project_submissions,
                s.is_verified() or s.user == self.alice,
                'Alice should only see verified submissions and her own.'
            )

    def assert_contains_submission(self, response, func=None):
        for s in self.submissions:
            if not func or func(s):
                self.assertContains(response, s.url)
            else:
                self.assertNotContains(response, s.url)

    def test_no_user_views_only_verified_submission(self):
        response = self.client.get(self.project.get_absolute_url())
        self.assert_contains_submission(response, lambda s: s.is_verified())

    def test_admin_views_all_submissions(self):
        login_user(self.client, self.admin)
        response = self.client.get(self.project.get_absolute_url())
        self.assert_contains_submission(response)

    def test_alice_views_verified_submissions_and_hers(self):
        login_user(self.client, self.alice)
        response = self.client.get(self.project.get_absolute_url())
        self.assert_contains_submission(response, lambda s: s.is_verified() or s.user == self.alice)

class TestCreateProjectSubmission(TestCase):
    def setUp(self):
        profiles.test_helpers.setup_alice_and_ada_test(self)
        self.project = test_helpers.make_project(self.alice, self.admin)
        self.submission_create_url = reverse('projects:create-submission', args=(self.project.pk,))

    def test_login_requirement(self):
        profiles.test_helpers.test_login_redirect(self, self.submission_create_url)

    def test_verified_email_requirement(self):
        profiles.test_helpers.test_verified_email_requirement(self,
            path     = self.submission_create_url,
            template = 'projects/submission_form.html')
