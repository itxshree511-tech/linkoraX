from django.db import models
from django.conf import settings
import uuid


class WithdrawRequest(models.Model):
    class WithdrawMethod(models.TextChoices):
        JAZZCASH = 'jazzcash', 'JazzCash'
        EASYPAISA = 'easypaisa', 'Easypaisa'
        
    class WithdrawStatus(models.TextChoices):
        PENDING = 'pending', 'Pending'
        APPROVED = 'approved', 'Approved'
        REJECTED = 'rejected', 'Rejected'
        PAID = 'paid', 'Paid'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='withdrawals')
    
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    withdraw_method = models.CharField(max_length=20, choices=WithdrawMethod.choices)
    
    account_number = models.CharField(max_length=20)
    account_holder = models.CharField(max_length=200)
    
    status = models.CharField(max_length=20, choices=WithdrawStatus.choices, default=WithdrawStatus.PENDING)
    
    notes = models.TextField(blank=True, null=True)
    admin_notes = models.TextField(blank=True, null=True)
    
    processed_at = models.DateTimeField(blank=True, null=True)
    processed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='processed_withdrawals')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'withdraw_requests'
        verbose_name = 'Withdraw Request'
        verbose_name_plural = 'Withdraw Requests'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.email} - {self.amount} PKR - {self.status}"
