from django.test import TestCase
from django.core.urlresolvers import reverse
from profiles.test_helpers import login_user, unverified_user, verified_user
from .test_helpers import ProjectFactory
from . import test_helpers
import profiles.test_helpers

class TestCreateProjectPermissions(TestCase):
    def test_login_requirement(self):
        profiles.test_helpers.test_login_redirect(self, reverse('projects:create'))

    def test_verified_email_requirement(self):
        profiles.test_helpers.test_verified_email_requirement(self,
            path     = reverse('projects:create'),
            template = 'projects/project_form.html')

    def test_verified_user_shows_form(self):
        p = verified_user()
        login_user(self.client, p)
        response = self.client.get(reverse('projects:create'))
        self.assertTemplateUsed(response, 'projects/project_form.html')

class TestProjectDisplayBasedOnPermissions(TestCase):
    def setUp(self):
        profiles.test_helpers.setup_alice_and_ada_test(self)

        # Alice and Ada each have a project that has been verified by an admin
        # and one that has not.
        self.projects = [
            test_helpers.make_project(self, self.ada),
            test_helpers.make_project(self, self.ada, self.admin),
            test_helpers.make_project(self, self.alice),
            test_helpers.make_project(self, self.alice, self.admin),
        ]

    def test_show_format_options(self):
        response = self.client.get(reverse('projects:index'))
        self.assertContains(response, '?format=table')

    def test_show_table_format(self):
        response = self.client.get('{}?format=table'.format(reverse('projects:index')))
        self.assertTemplateUsed(response, 'projects/_project_list_table.html')
        self.assertTemplateNotUsed(response, 'projects/_project_list_cards.html')

    def test_show_cards_format(self):
        response = self.client.get(reverse('projects:index'))
        self.assertTemplateUsed(response, 'projects/_project_list_cards.html')
        self.assertTemplateNotUsed(response, 'projects/_project_list_table.html')

    def assert_contains_project_name(self, response, func=None):
        for p in self.projects:
            if not func or func(p):
                self.assertContains(response, p.name)
            else:
                self.assertNotContains(response, p.name)

    def test_admin_sees_all_projects(self):
        login_user(self.client, self.admin)
        response = self.client.get(reverse('projects:index'))
        self.assert_contains_project_name(response)

    def test_alice_sees_correct_projects(self):
        # Alice should only see verified projects or her own unverified ones.
        login_user(self.client, self.alice)
        response = self.client.get(reverse('projects:index'))
        self.assert_contains_project_name(response, lambda p: p.is_verified() or p.user == self.alice)

    def test_public_sees_only_verified_projects(self):
        response = self.client.get(reverse('projects:index'))
        self.assert_contains_project_name(response, lambda p: p.is_verified())

class TestProjectEditing(TestCase):
    def setUp(self):
        profiles.test_helpers.setup_alice_and_ada_test(self)
        self.project = test_helpers.make_project(self, self.alice, self.admin)
        self.project_update_url = reverse('projects:update', args=(self.project.pk,))

    def check_edit_button(self, check_contains):
        response = self.client.get(self.project.get_absolute_url())
        if check_contains:
            self.assertContains(response, self.project_update_url)
        else:
            self.assertNotContains(response, self.project_update_url)

    def test_show_edit_button_to_moderator(self):
        login_user(self.client, self.admin)
        self.check_edit_button(True)

    def test_show_edit_button_to_project_owner(self):
        login_user(self.client, self.alice)
        self.check_edit_button(True)

    def test_dont_show_edit_button_to_other_users(self):
        self.check_edit_button(False)
        login_user(self.client, self.ada)
        self.check_edit_button(False)

    def test_permission_project_owner(self):
        login_user(self.client, self.alice)
        response = self.client.get(self.project_update_url)
        self.assertEqual(response.status_code, 200)

    def test_permission_moderator(self):
        login_user(self.client, self.admin)
        response = self.client.get(self.project_update_url)
        self.assertEqual(response.status_code, 200)

    def test_permission_redirects(self):
        response = self.client.get(self.project_update_url)
        self.assertEqual(response.status_code, 302)
        login_user(self.client, self.ada)
        response = self.client.get(self.project_update_url)
        self.assertEqual(response.status_code, 302)
