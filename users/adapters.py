from allauth.account.adapter import DefaultAccountAdapter
from django.urls import reverse


class CustomAccountAdapter(DefaultAccountAdapter):
    def get_login_redirect_url(self, request):
        user = request.user
        if user.groups.filter(name='Django Admin').exists():
            return reverse('admin:index')
        elif user.groups.filter(name='Site Admin').exists():
            return reverse('users:admin_reports')
        return reverse('users:home')

