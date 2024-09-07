from django.forms import ValidationError
from django.test import TestCase
from django.utils import timezone

from users.models import Report, StandardOfConduct
from .factories import ReportFactory

class StandardOfConductTests(TestCase):
  def test_fails_to_create_standard_of_conduct_with_invalid_standard(self):
    with self.assertRaises(ValidationError):
      standard = StandardOfConduct.objects.create(standard=0)
      standard.clean()

class ReportTests(TestCase):
  def test_create_report(self):
    report = ReportFactory()
    self.assertEqual(report.name_of_reporter, "John Doe")
    self.assertTrue(report.violated_standards_conduct.exists())
    self.assertEqual(report.status, "new")

  def test_report_with_future_date_of_incident_is_invalid(self):
    with self.assertRaises(ValidationError):
      tomorrow = timezone.now() + timezone.timedelta(days=1)
      report = ReportFactory(date_of_incident=tomorrow.date())
      report.clean_fields()
