from django.test import TestCase
from django.utils import timezone
from django.core.urlresolvers import reverse
from profiles.test_helpers import login_user, verified_user
from projects.models import Project, Submission
from .test_helpers import ProjectFactory, SubmissionFactory
from . import test_helpers
import profiles.test_helpers

class TestVerificationModel(TestCase):
    def test_is_not_verified(self):
        p = ProjectFactory(user=verified_user())
        self.assertFalse(p.is_verified())

    def test_is_verified(self):
        p = ProjectFactory(
                user=verified_user(),
                verified_by=verified_user(is_staff=True),
                verified_date=timezone.now())
        self.assertTrue(p.is_verified())

    def test_will_toggle_verify(self):
        p = ProjectFactory(user=verified_user())
        a = verified_user(is_staff=True)
        p.toggle_verify(a)
        self.assertTrue(p.is_verified())
        p.toggle_verify(a)
        self.assertFalse(p.is_verified())

def verify_model_with_assertions(test, model, model_cls):
    model_name = model_cls.__name__

    login_user(test.client, test.admin)
    response = test.client.post(model.get_verify_url())

    test.assertTrue(
        response['Location'].endswith(model.get_absolute_url()),
        'Verification toggle did not redirect back to {} page.'.format(model_name)
    )
    m = model_cls.objects.get(pk=model.pk)
    test.assertTrue(m.is_verified(), '{} did not receive verification.'.format(model_name))
    test.assertEqual(m.verified_by, test.admin, '{} was verified by the wrong user.'.format(model_name))

def toggle_project_to_unverified_with_assertions(test, model, model_cls):
    model_name = model_cls.__name__

    login_user(test.client, test.admin)
    response = test.client.post(model.get_verify_url())
    test.assertTrue(
        response['Location'].endswith(model.get_absolute_url()),
        'Verification toggle did not redirect back to the {} page.'.format(model_name)
    )
    test.assertFalse(model_cls.objects.get(pk=model.pk).is_verified(), '{} is still verified after attempt to remove verification.'.format(model_name))

class TestProjectVerification(TestCase):
    def setUp(self):
        profiles.test_helpers.setup_alice_and_ada_test(self)
        self.project = ProjectFactory(user=self.alice)
        self.verify_path = self.project.get_verify_url()

    def test_no_get_params(self):
        login_user(self.client, self.admin)
        response = self.client.post(reverse('projects:verify'))
        self.assertEqual(response.status_code, 404,
            'Verification request should 404 if GET parameters do not specify a model.')

    def test_invalid_model_get_param(self):
        login_user(self.client, self.admin)
        response = self.client.post('{}?model=Vouch'.format(reverse('projects:verify')))
        self.assertEqual(response.status_code, 404,
            'Verification request should 404 if GET parameters specify an invalid model.')

    def test_show_verify_button_to_moderator(self):
        login_user(self.client, self.admin)
        response = self.client.get(self.project.get_absolute_url())
        self.assertContains(response, self.verify_path,
            msg_prefix='Moderator was not shown verification button.')

    def test_hide_verify_button_from_others(self):
        login_user(self.client, self.alice)
        response = self.client.get(self.project.get_absolute_url())
        self.assertNotContains(response, self.verify_path,
            msg_prefix='Verification button should only be shown to moderators.')

    def test_verify_redirect_if_not_logged_in(self):
        project  = ProjectFactory(user=self.alice)
        response = self.client.post(project.get_verify_url())
        self.assertEqual(response.status_code, 302,
            'Verification request should redirect if no user is logged in.')

        self.assertFalse(project.is_verified(), 'Project should not be verified on permission failure.')

    def test_verify_redirect_if_not_moderator(self):
        login_user(self.client, self.alice)
        project  = ProjectFactory(user=self.alice)
        response = self.client.post(project.get_verify_url())
        self.assertEqual(response.status_code, 302,
            'Verification request should redirect if a moderator is not logged in.')

        self.assertFalse(project.is_verified(), 'Project should not be verified on permission failure.')

    def test_verify_project(self):
        verify_model_with_assertions(self, ProjectFactory(user=self.alice), Project)

    def test_toggle_project_to_unverified(self):
        p = test_helpers.make_project(self, self.alice, self.admin)
        toggle_project_to_unverified_with_assertions(self, p, Project)

class TestSubmissionVerification(TestCase):
    def setUp(self):
        profiles.test_helpers.setup_alice_and_ada_test(self)
        self.project = test_helpers.make_project(self, self.alice, self.admin)
        self.submission = SubmissionFactory(user=self.alice, project=self.project)
        self.verify_path = self.submission.get_verify_url()

    def test_verify_submission(self):
        s = test_helpers.make_submission_on_project(self, self.alice)
        verify_model_with_assertions(self, s, Submission)

    def test_toggle_submission_to_unverified(self):
        s = test_helpers.make_submission_on_project(self, self.alice, self.admin)
        toggle_project_to_unverified_with_assertions(self, s, Submission)
