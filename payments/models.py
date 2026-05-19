from django.db import models
from django.conf import settings
import uuid


class MembershipPayment(models.Model):
    class PaymentMethod(models.TextChoices):
        JAZZCASH = 'jazzcash', 'JazzCash'
        EASYPAISA = 'easypaisa', 'Easypaisa'
        PAYFAST = 'payfast', 'PayFast'
        
    class PaymentStatus(models.TextChoices):
        PENDING = 'pending', 'Pending'
        PROCESSING = 'processing', 'Processing'
        APPROVED = 'approved', 'Approved'
        REJECTED = 'rejected', 'Rejected'
        FAILED = 'failed', 'Failed'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='payments')
    
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PaymentMethod.choices)
    
    status = models.CharField(max_length=20, choices=PaymentStatus.choices, default=PaymentStatus.PENDING)
    
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    receipt_image = models.ImageField(upload_to='payment_receipts/', blank=True, null=True)
    
    notes = models.TextField(blank=True, null=True)
    admin_notes = models.TextField(blank=True, null=True)
    
    processed_at = models.DateTimeField(blank=True, null=True)
    processed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='processed_payments')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'membership_payments'
        verbose_name = 'Membership Payment'
        verbose_name_plural = 'Membership Payments'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.email} - {self.amount} PKR - {self.status}"
