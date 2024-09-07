from django.test import TestCase
from django.urls import reverse

from .factories import ReportFactory, UserFactory, SocialAccountFactory

class HomePageTests(TestCase):
  def test_logging_in_with_google_redirects(self):
    # simulate pressing the login with google button
    response = self.client.get('/accounts/google/login/')
    self.assertEqual(response.status_code, 302)

  def test_logged_in_user(self):
    self.user = UserFactory(username="testuser", first_name="Test", last_name="User")
    self.social_account = SocialAccountFactory(user=self.user)
    self.client.login(username="testuser", password="testpassword")
    response = self.client.get(reverse("users:home"))
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, "File a report as Test User")
    self.assertContains(response, "My Reports")
    self.assertContains(response, "Log out")
    self.assertNotContains(response, "Manage Reports")

  def test_anonymous_user(self):
    response = self.client.get(reverse("users:home"))
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, "File an anonymous report")
    self.assertNotContains(response, "Manage Reports")

class NewReportPageTests(TestCase):
  def test_logged_in_user_view(self):
    self.user = UserFactory(username="testuser", first_name="Test", last_name="User")
    self.social_account = SocialAccountFactory(user=self.user)
    self.client.login(username="testuser", password="testpassword")
    response = self.client.get(reverse("users:file_report"))
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, "You are logged in as Test User")

  def test_anonymous_user_view(self):
    response = self.client.get(reverse("users:file_report"))
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, "You are reporting anonymously")

  def test_user_submits_report(self):
    report = ReportFactory()
    response = self.client.get(reverse("users:report_submitted", args=[report.id]))
    self.assertEqual(response.status_code, 200)

    home_url = reverse("users:home")
    self.assertContains(response, "Return to home")
    self.assertContains(response, f"href=\"{home_url}\"")

class AdminReportsPageTests(TestCase):
  def test_anonymous_user_cant_view_reports(self):
    response = self.client.get(reverse("users:admin_reports"))
    self.assertEqual(response.status_code, 302)
    self.assertRedirects(response, reverse("users:home") + "?next=" + reverse("users:admin_reports"))

  def test_regular_user_cant_view_reports(self):
    self.user = UserFactory(username="testuser", first_name="Test", last_name="User")
    self.social_account = SocialAccountFactory(user=self.user)
    self.client.login(username="testuser", password="testpassword")
    response = self.client.get(reverse("users:admin_reports"))
    self.assertEqual(response.status_code, 302)
    self.assertRedirects(response, reverse("users:home") + "?next=" + reverse("users:admin_reports"))

  def test_site_admin_can_view_reports(self):
    self.user = UserFactory(username="testuser", groups=["Site Admin"])
    self.social_account = SocialAccountFactory(user=self.user)
    self.client.login(username="testuser", password="testpassword")
    response = self.client.get(reverse("users:admin_reports"))
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, "Manage Reports")
    self.assertContains(response, "Submitted Reports")
    self.assertContains(response, "No reports have been submitted yet.")

    # make an anonymous report to show
    anonymous_report = ReportFactory(name_of_reporter="", email_of_reporter="")
    response = self.client.get(reverse("users:admin_reports"))
    self.assertNotContains(response, "Reporter Name")
    self.assertNotContains(response, "Email")
    self.assertContains(response, "Show Details")
    self.assertContains(response, "Phone")
    self.assertContains(response, "Organization")
    self.assertContains(response, "Date of Incident")
    self.assertContains(response, "Time of Incident")
    self.assertContains(response, "Location")
    self.assertContains(response, "Description")
    self.assertContains(response, "Date Submitted")

    # make a new signed-in user report to show
    user_report = ReportFactory()
    response = self.client.get(reverse("users:admin_reports"))
    self.assertContains(response, "Reporter Name")
    self.assertContains(response, "Email")
    self.assertContains(response, "Submit Comment")
    self.assertContains(response, "Update Status")

class UserReportsPageTests(TestCase):
  def test_anonymous_user_cant_view_reports(self):
    response = self.client.get(reverse("users:user_reports"))
    self.assertEqual(response.status_code, 302)
    self.assertRedirects(response, reverse("users:home") + "?next=" + reverse("users:user_reports"))

  def test_logged_in_user_can_view_reports(self):
    self.user = UserFactory(username="testuser", first_name="Test", last_name="User")
    self.social_account = SocialAccountFactory(user=self.user)
    self.client.login(username="testuser", password="testpassword")
    response = self.client.get(reverse("users:user_reports"))
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, "Your Reports")
    self.assertContains(response, "No reports found.")

    # make a new report to show
    report = ReportFactory(email_of_reporter=self.user.email, name_of_reporter=self.user.get_full_name())
    response = self.client.get(reverse("users:user_reports"))
    self.assertContains(response, "Test User")
    self.assertContains(response, "New")
    self.assertContains(response, "Show Details")
    self.assertContains(response, "Retract Report")
