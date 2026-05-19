from django.db import models
from django.conf import settings
import uuid


class FraudLog(models.Model):
    class FraudType(models.TextChoices):
        SELF_REFERRAL = 'self_referral', 'Self Referral'
        DUPLICATE_IP = 'duplicate_ip', 'Duplicate IP'
        SUSPICIOUS_ACTIVITY = 'suspicious_activity', 'Suspicious Activity'
        MULTIPLE_ACCOUNTS = 'multiple_accounts', 'Multiple Accounts'
        PAYMENT_FRAUD = 'payment_fraud', 'Payment Fraud'
        WITHDRAWAL_FRAUD = 'withdrawal_fraud', 'Withdrawal Fraud'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='fraud_logs', blank=True, null=True)
    
    fraud_type = models.CharField(max_length=50, choices=FraudType.choices)
    description = models.TextField()
    
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.TextField(blank=True, null=True)
    
    severity = models.CharField(max_length=20, choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')], default='medium')
    
    is_resolved = models.BooleanField(default=False)
    action_taken = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'fraud_logs'
        verbose_name = 'Fraud Log'
        verbose_name_plural = 'Fraud Logs'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.fraud_type} - {self.user.email if self.user else 'Unknown'}"


class SuspiciousIP(models.Model):
    ip_address = models.GenericIPAddressField(unique=True)
    
    attempt_count = models.IntegerField(default=0)
    is_blocked = models.BooleanField(default=False)
    
    notes = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'suspicious_ips'
        verbose_name = 'Suspicious IP'
        verbose_name_plural = 'Suspicious IPs'
    
    def __str__(self):
        return f"{self.ip_address} - {'Blocked' if self.is_blocked else 'Not Blocked'}"
