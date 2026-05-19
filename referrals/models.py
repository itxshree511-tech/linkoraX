from django.db import models
from django.conf import settings
import uuid


class Referral(models.Model):
    class ReferralLevel(models.IntegerChoices):
        LEVEL_1 = 1, 'Level 1'
        LEVEL_2 = 2, 'Level 2'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    referrer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='referrals_made')
    referred = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='referral_received')
    
    level = models.IntegerField(choices=ReferralLevel.choices, default=ReferralLevel.LEVEL_1)
    
    commission_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    commission_paid = models.BooleanField(default=False)
    
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.TextField(blank=True, null=True)
    
    is_suspicious = models.BooleanField(default=False)
    fraud_notes = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'referrals'
        verbose_name = 'Referral'
        verbose_name_plural = 'Referrals'
        ordering = ['-created_at']
        unique_together = ['referred']
    
    def __str__(self):
        return f"{self.referrer.email} -> {self.referred.email} (Level {self.level})"


class ReferralStats(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='referral_stats')
    
    total_referrals = models.IntegerField(default=0)
    level_1_count = models.IntegerField(default=0)
    level_2_count = models.IntegerField(default=0)
    
    total_commissions = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    level_1_commissions = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    level_2_commissions = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    active_referrals = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'referral_stats'
        verbose_name = 'Referral Stats'
        verbose_name_plural = 'Referral Stats'
    
    def __str__(self):
        return f"{self.user.email} - Stats"
