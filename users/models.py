from .managers import UserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
import uuid


class User(AbstractUser):
    class UserRole(models.TextChoices):
        MEMBER = 'member', _('Member')
        ADMIN = 'admin', _('Admin')
        SUPER_ADMIN = 'super_admin', _('Super Admin')

    class AccountStatus(models.TextChoices):
        ACTIVE = 'active', _('Active')
        SUSPENDED = 'suspended', _('Suspended')
        FROZEN = 'frozen', _('Frozen')
        PENDING_VERIFICATION = 'pending_verification', _('Pending Verification')

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = None  # Remove username, use email instead
    email = models.EmailField(_('email address'), unique=True)
    
    role = models.CharField(max_length=20, choices=UserRole.choices, default=UserRole.MEMBER)
    account_status = models.CharField(max_length=30, choices=AccountStatus.choices, default=AccountStatus.PENDING_VERIFICATION)
    
    phone = models.CharField(max_length=20, blank=True, null=True)
    phone_verified = models.BooleanField(default=False)
    
    email_verified = models.BooleanField(default=False)
    
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    
    referral_code = models.CharField(max_length=20, unique=True, blank=True, null=True)
    
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.TextField(blank=True, null=True)
    
    last_activity = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    class Meta:
        db_table = 'users'
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        ordering = ['-created_at']
    
    def __str__(self):
        return self.email
    
    def save(self, *args, **kwargs):
        if not self.referral_code:
            self.referral_code = self.generate_referral_code()
        super().save(*args, **kwargs)
    
    def generate_referral_code(self):
        import random
        import string
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        while User.objects.filter(referral_code=code).exists():
            code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        return code


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    full_name = models.CharField(max_length=200, blank=True)
    
    country = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    address = models.TextField(blank=True)
    
    date_of_birth = models.DateField(blank=True, null=True)
    
    cnic = models.CharField(max_length=15, blank=True, null=True)
    
    jazzcash_number = models.CharField(max_length=15, blank=True, null=True)
    easypaisa_number = models.CharField(max_length=15, blank=True, null=True)
    
    bio = models.TextField(blank=True)
    
    social_facebook = models.URLField(blank=True)
    social_twitter = models.URLField(blank=True)
    social_linkedin = models.URLField(blank=True)
    
    notification_email = models.BooleanField(default=True)
    notification_sms = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'user_profiles'
        verbose_name = _('User Profile')
        verbose_name_plural = _('User Profiles')
    
    def __str__(self):
        return f"{self.user.email} - Profile"
