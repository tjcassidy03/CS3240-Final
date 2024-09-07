from django.contrib import admin
from django import forms
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from django.contrib.auth.models import User, Group


class UserAdminForm(forms.ModelForm):
    is_siteadmin = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        super(UserAdminForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['is_siteadmin'].initial = self.instance.groups.filter(name='Site Admin').exists()

    def save(self, *args, **kwargs):
        user = super(UserAdminForm, self).save(*args, **kwargs)
        if self.cleaned_data['is_siteadmin']:
            user.groups.add(Group.objects.get(name='Site Admin'))
        else:
            user.groups.remove(Group.objects.get(name='Site Admin'))
        return user

    class Meta:
        model = User
        fields = '__all__'

class UserAdmin(DefaultUserAdmin):
    form = UserAdminForm

    def add_to_siteadmin_group(self, request, queryset):
        siteadmin_group = Group.objects.get(name='Site Admin')
        for user in queryset:
            user.groups.add(siteadmin_group)

    add_to_siteadmin_group.short_description = "Add selected users to Site Admin group"

    actions = [add_to_siteadmin_group]


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
