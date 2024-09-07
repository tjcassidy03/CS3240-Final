from django.test import TestCase
from .factories import UserFactory, SocialAccountFactory

class UserFactoryTests(TestCase):
  def test_create_user(self):
    user = UserFactory(email="example@example.com", groups=["Site Admin"])
    self.assertEqual(user.email, "example@example.com")
    self.assertTrue(user.groups.filter(name="Site Admin"))

class SocialAccountFactoryTests(TestCase):
  def test_create_social_account(self):
    user = UserFactory(username="testuser")
    social_account = SocialAccountFactory(user=user)
    self.assertEqual(social_account.user, user)
    self.assertEqual(social_account.provider, "google")
