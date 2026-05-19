from allauth.account.adapter import DefaultAccountAdapter
from django.conf import settings


class CustomAccountAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form, commit=True):
        user = super().save_user(request, user, form, commit=False)
        
        # Set custom fields
        if 'phone' in form.cleaned_data:
            user.phone = form.cleaned_data['phone']
        
        if commit:
            user.save()
        
        return user
