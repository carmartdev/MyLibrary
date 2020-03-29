from django.contrib.admin.sites import AdminSite
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.test import TestCase
from store.admin import SessionAdmin

class MockRequest:
    pass

class SessionAdminTest(TestCase):
    def user_can_see_another_user_session(self, observer, observable):
        self.client.force_login(observable)
        self.client.get("/")

        session_admin = SessionAdmin(model=Session, admin_site=AdminSite())
        mock_request = MockRequest()
        mock_request.user = observer
        user_ids = [session.get_decoded()["_auth_user_id"]
                    for session in session_admin.get_queryset(mock_request)]

        return str(observable.id) in user_ids

    def test_superuser_can_see_unprivileged_users_sessions(self):
        self.assertTrue(self.user_can_see_another_user_session(
            User.objects.create_superuser(username="Bob"),
            User.objects.create_user(username="Alice")))

    def test_superuser_can_see_staff_sessions(self):
        self.assertTrue(self.user_can_see_another_user_session(
            User.objects.create_superuser(username="Bob"),
            User.objects.create_user(username="Alice", is_staff=True)))

    def test_superuser_can_see_superusers_sessions(self):
        self.assertTrue(self.user_can_see_another_user_session(
            User.objects.create_superuser(username="Bob"),
            User.objects.create_superuser(username="Alice")))

    def test_staff_can_see_unprivileged_users_sessions(self):
        self.assertTrue(self.user_can_see_another_user_session(
            User.objects.create_user(username="Bob", is_staff=True),
            User.objects.create_user(username="Alice")))

    def test_staff_cant_see_other_staff_sessions(self):
        self.assertFalse(self.user_can_see_another_user_session(
            User.objects.create_user(username="Bob", is_staff=True),
            User.objects.create_user(username="Alice", is_staff=True)))

    def test_staff_cant_see_other_superusers_sessions(self):
        self.assertFalse(self.user_can_see_another_user_session(
            User.objects.create_user(username="Bob", is_staff=True),
            User.objects.create_superuser(username="Alice")))

    def test_unprivileged_users_cant_see_unprivileged_users_sessions(self):
        self.assertFalse(self.user_can_see_another_user_session(
            User.objects.create_user(username="Bob"),
            User.objects.create_user(username="Alice")))

    def test_unprivileged_users_cant_see_staff_sessions(self):
        self.assertFalse(self.user_can_see_another_user_session(
            User.objects.create_user(username="Bob"),
            User.objects.create_user(username="Alice", is_staff=True)))

    def test_unprivileged_users_cant_see_superusers_sessions(self):
        self.assertFalse(self.user_can_see_another_user_session(
            User.objects.create_user(username="Bob"),
            User.objects.create_superuser(username="Alice")))
