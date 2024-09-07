from users.models import Report, StandardOfConduct
from allauth.socialaccount.models import SocialAccount
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

import factory

class UserFactory(factory.django.DjangoModelFactory):
  class Meta:
    model = get_user_model()

  username = factory.Faker('user_name')
  email = factory.Faker('email')
  first_name = factory.Faker('first_name')
  last_name = factory.Faker('last_name')

  @factory.post_generation
  def password(self, create, extracted, **kwargs):
    self.set_password("testpassword")

  @factory.post_generation
  def groups(self, create, extracted, **kwargs):
    if extracted:
      for group in extracted:
        group, created = Group.objects.get_or_create(name=group)
        self.groups.add(group)

class SocialAccountFactory(factory.django.DjangoModelFactory):
  class Meta:
    model = SocialAccount

  user = factory.SubFactory(UserFactory)
  provider = 'google'
  uid = factory.Faker('uuid4')

class ReportFactory(factory.django.DjangoModelFactory):
  class Meta:
    model = Report

  name_of_reporter = "John Doe"
  email_of_reporter = "john@example.com"
  phone_num_of_reporter = "123-456-7890"
  organization_of_reporter = "IFC JC"
  date_of_incident = timezone.now().date()
  time_of_incident = timezone.now().time()
  location_of_incident = "Lambeth Field"
  description_of_event = "There were hazing activities involving drinking copious amounts of alcohol."
  name_of_accused_fraternity = "Alpha Beta"
  status = "new"

  @factory.post_generation
  def violated_standards_conduct(self, create, extracted, **kwargs):
    if not create or not extracted:
      # set a default violated_standards_conduct
      self.violated_standards_conduct.add(StandardOfConduct.objects.get(standard=13))
      return

    self.violated_standards_conduct.add(*extracted)
