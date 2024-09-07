from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone
from users.UserType import UserType
from storage_backends import MediaStorage


class User(models.Model):
    USER_TYPE_CHOICES = {
        (UserType.ANONYMOUS, "Anonymous"),
        (UserType.COMMON, "Common"),
        (UserType.IFC_ADMIN, "IFC JC Admin"),
        (UserType.IFC_COUNSELOR, "IFC JC Counselor"),
        (UserType.DJANGO_ADMIN, "Django Admin")
    }

    rolls = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default=UserType.COMMON)


class StandardOfConduct(models.Model):
    STANDARD_DESCRIPTIONS = {
        1: 'Physical abuse of any person on fraternity owned or controlled property or at fraternity sponsored or supervised functions, or conduct which threatens or endangers the health or safety of any person.',
        2: 'Damage to fraternity property, or property owned by a member of a fraternity, or to a visitor or guest of a fraternity.',
        3: 'Unauthorized entry into or occupation of fraternity facilities that are locked, closed to student activities, or otherwise restricted to use.',
        4: 'Unlawfully blocking or impeding normal pedestrian or vehicular traffic on or adjacent to fraternity property.',
        5: 'Disorderly conduct on fraternity owned, operated, or controlled property or at fraternity sponsored functions. This includes but is not limited to acts that breach the peace, or are deemed lewd, indecent or obscene, as well as excessive noise.',
        6: 'Conduct that is incompatible with the good character and personal responsibility expected of all members of the fraternity community and that dishonors the fraternity system at the University of Virginia.',
        7: 'Violations of University policies and procedures referenced in the FOA.',
        8: 'Failing to comply with the IFC Standards for Parties and Social Events.',
        9: 'Failing to comply with the IFC Rush Regulations.',
        10: 'Failing to comply with city/county ordinances governing residences, including garbage, shoveling snow from sidewalks, and noise levels.',
        11: 'Any violation of Federal, State, or Local law that directly affects the University’s pursuit of its proper educational purposes to the extent such violations are not covered by other Standards of Conduct.',
        12: 'Conduct that intentionally violates the rules of confidentiality or obstructs the operations of the IFCJC.',
        13: 'Hazing in violation of the Virginia statute or University regulations.',
        14: 'Failing to comply with directions of IFC officials acting under provisions 1-13 set out above.'
    }

    standard = models.IntegerField(unique=True, validators=[MinValueValidator(1), MaxValueValidator(14)])

    def clean(self):
        if not 1 <= self.standard <= 14:
            raise ValidationError('Standard must be an integer between 1 and 14.')

    def __str__(self):
        return f"{self.standard}. {self.STANDARD_DESCRIPTIONS.get(self.standard, 'Unknown Standard')}"


class Report(models.Model):
    def validate_date_of_incident(value):
        if value > timezone.now().date():
            raise ValidationError('Date of incident cannot be in the future.')

    STATUS_CHOICES = (
        ('new', 'New'),
        ('in progress', 'In Progress'),
        ('resolved', 'Resolved')
    )

    # fields without `blank=True` are required
    # db auto-populates fields changed from null=True to null=False with specified default values
    name_of_reporter = models.CharField(max_length=100, blank=True, default="")
    email_of_reporter = models.EmailField(blank=True, default="")
    phone_num_of_reporter = models.CharField(max_length=20, blank=True, default="")
    organization_of_reporter = models.CharField(max_length=100, blank=True, default="")
    date_of_incident = models.DateField(validators=[validate_date_of_incident])
    time_of_incident = models.TimeField()
    location_of_incident = models.CharField(max_length=150, default="")
    description_of_event = models.TextField()
    name_of_accused_fraternity = models.CharField(max_length=100, default="")
    violated_standards_conduct = models.ManyToManyField(StandardOfConduct)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new', null=True)
    admin_comment = models.TextField(blank=True, null=True)
    reviewer_comments = models.TextField(null=True, blank=True, default='No review yet')

    def __str__(self):
        return f"Report number {self.id} by {self.name_of_reporter} on {self.date_of_incident}"


class ReportFile(models.Model):
    report = models.ForeignKey(Report, related_name='files', on_delete=models.CASCADE)
    file = models.FileField(blank=True, null=True, upload_to='uploads/', storage=MediaStorage())

    def __str__(self):
        return f"Uploaded file {self.file.name} for Report ID: {self.report.id}"
