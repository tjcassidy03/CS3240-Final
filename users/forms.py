from django import forms
from .models import Report, ReportFile, StandardOfConduct


class ReportForm(forms.ModelForm):
    violated_standards_conduct = forms.ModelMultipleChoiceField(
        queryset=StandardOfConduct.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label=''
    )

    phone_num_of_reporter = forms.CharField(
        widget=forms.TextInput(attrs={'type': 'tel', 'placeholder': 'Phone Number'}),
        required=False,
        label='Phone Number',
        help_text='Your phone number (optional)'
    )

    class Meta:
        model = Report
        fields = [
            'name_of_reporter',
            'email_of_reporter',
            'phone_num_of_reporter',
            'date_of_incident',
            'time_of_incident',
            'organization_of_reporter',
            'location_of_incident',
            'name_of_accused_fraternity',
            'description_of_event',
            'violated_standards_conduct'
        ]
        widgets = {
            'date_of_incident': forms.DateInput(attrs={'type': 'date'}),
            'time_of_incident': forms.TimeInput(attrs={'type': 'time'}),
        }
        labels = {
            'date_of_incident': 'Date of the incident',
            'organization_of_reporter': 'If you are part of a fraternity provide the name here',
            'location_of_incident': 'Location of the incident',
            'time_of_incident': 'Time of the incident',
            'name_of_accused_fraternity': 'Name of accused fraternity'
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(ReportForm, self).__init__(*args, **kwargs)
        if user and user.is_authenticated:
            self.fields['name_of_reporter'].initial = user.get_full_name()
            self.fields['email_of_reporter'].initial = user.email
            self.fields['name_of_reporter'].widget = forms.HiddenInput()
            self.fields['email_of_reporter'].widget = forms.HiddenInput()
        else:
            del self.fields['name_of_reporter']
            del self.fields['email_of_reporter']
        required_fields = ['date_of_incident', 'time_of_incident', 'location_of_incident', 'name_of_accused_fraternity', 'description_of_event']
        for field_name in required_fields:
            field = self.fields.get(field_name)
            if field:
                field.required = True
                field.label = f"*{field.label}"


    def clean(self):
        cleaned_data = super().clean()
        standards = cleaned_data.get('violated_standards_conduct')
        return cleaned_data

class UploadFileForm(forms.ModelForm):
    class Meta:
        model = ReportFile
        fields = [
            'file'
        ]

class AdminCommentForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['admin_comment']
        labels = {
            'admin_comment': 'Admin Comment'
        }

class ReportStatusForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['status']

