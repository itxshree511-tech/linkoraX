from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, UserProfile


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            'placeholder': 'Enter your email'
        })
    )
    phone = forms.CharField(
        required=False,
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            'placeholder': 'Phone number (optional)'
        })
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            'placeholder': 'Create password'
        })
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            'placeholder': 'Confirm password'
        })
    )
    
    class Meta:
        model = User
        fields = ('email', 'phone', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'autofocus': False})


class UserLoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            'placeholder': 'Enter your email'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            'placeholder': 'Enter your password'
        })
    )


class UserProfileForm(forms.ModelForm):
    avatar = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg', 'accept': 'image/*'})
    )

    class Meta:
        model = UserProfile
        fields = [
            'full_name', 'country', 'city', 'address', 'date_of_birth',
            'cnic', 'jazzcash_number', 'easypaisa_number', 'bio',
            'social_facebook', 'social_twitter', 'social_linkedin',
            'notification_email', 'notification_sms'
        ]
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg'}),
            'country': forms.TextInput(attrs={'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg'}),
            'city': forms.TextInput(attrs={'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg'}),
            'address': forms.Textarea(attrs={'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg', 'rows': 3}),
            'date_of_birth': forms.DateInput(attrs={'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg', 'type': 'date'}),
            'cnic': forms.TextInput(attrs={'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg'}),
            'jazzcash_number': forms.TextInput(attrs={'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg'}),
            'easypaisa_number': forms.TextInput(attrs={'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg'}),
            'bio': forms.Textarea(attrs={'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg', 'rows': 4}),
            'social_facebook': forms.URLInput(attrs={'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg'}),
            'social_twitter': forms.URLInput(attrs={'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg'}),
            'social_linkedin': forms.URLInput(attrs={'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        profile = super().save(commit=commit)
        if self.user and self.cleaned_data.get('avatar') is not None:
            self.user.avatar = self.cleaned_data.get('avatar')
            if commit:
                self.user.save(update_fields=['avatar', 'updated_at'])
        return profile
