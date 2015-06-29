from django.test import TestCase
from django.core.urlresolvers import reverse
from profiles.test_helpers import login_user, unverified_user, verified_user
from .test_helpers import ProjectFactory

class TestCreateProjectPermissions(TestCase):
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

class TestProjectDisplayBasedOnPermissions(TestCase):
    def setUp(self):
        self.admin   = verified_user(is_staff=True)
        self.alice   = verified_user()
        self.ada     = verified_user()

        # Alice and Ada each have a project that has been verified by an admin
        # and one that has not.
        self.unverified_ada_project   = ProjectFactory(user=self.ada, name='Unverified Ada Project')
        self.verified_ada_project     = ProjectFactory(user=self.ada, name='Verified Ada Project')
        self.verified_ada_project.toggle_verify(self.admin)

        self.unverified_alice_project = ProjectFactory(user=self.alice, name='Unverified Alice Project')
        self.verified_alice_project   = ProjectFactory(user=self.alice, name='Verified Alice Project')
        self.verified_alice_project.toggle_verify(self.admin)

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


    def test_admin_sees_all_projects(self):
        login_user(self.client, self.admin)
        response = self.client.get(reverse('projects:index'))
        self.assertContains(response, self.verified_ada_project.name)
        self.assertContains(response, self.verified_alice_project.name)
        self.assertContains(response, self.unverified_ada_project.name)
        self.assertContains(response, self.unverified_alice_project.name)

    def test_alice_sees_correct_projects(self):
        login_user(self.client, self.alice)
        response = self.client.get(reverse('projects:index'))
        self.assertContains(response, self.verified_ada_project.name)
        self.assertContains(response, self.verified_alice_project.name)
        self.assertContains(response, self.unverified_alice_project.name, msg_prefix='Alice should see her own unverified project.')
        self.assertNotContains(response, self.unverified_ada_project.name, msg_prefix="Alice should not see Ada's unverified project.")

    def test_public_sees_only_verified_projects(self):
        response = self.client.get(reverse('projects:index'))
        self.assertContains(response, self.verified_ada_project.name)
        self.assertContains(response, self.verified_alice_project.name)
        self.assertNotContains(response, self.unverified_ada_project.name)
        self.assertNotContains(response, self.unverified_alice_project.name)

class TestProjectEditing(TestCase):
    def setUp(self):
        self.admin = verified_user(is_staff=True)
        self.alice = verified_user()
        self.ada   = verified_user()
        self.project = ProjectFactory(user=self.alice, name='Verified Alice Project')
        self.project.toggle_verify(self.admin)
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
