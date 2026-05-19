from django.contrib import admin
from django import forms
from django.utils import timezone
from .models import MembershipPayment


class MembershipPaymentAdminForm(forms.ModelForm):
    class Meta:
        model = MembershipPayment
        fields = '__all__'

    def clean(self):
        cleaned = super().clean()
        status = cleaned.get('status')
        admin_notes = (cleaned.get('admin_notes') or '').strip()
        if status in {
            MembershipPayment.PaymentStatus.APPROVED,
            MembershipPayment.PaymentStatus.REJECTED,
            MembershipPayment.PaymentStatus.FAILED,
        } and not admin_notes:
            raise forms.ValidationError('Admin notes are required when approving/rejecting/failing a payment.')
        return cleaned


@admin.register(MembershipPayment)
class MembershipPaymentAdmin(admin.ModelAdmin):
    form = MembershipPaymentAdminForm
    list_display = ('user', 'amount', 'payment_method', 'status', 'transaction_id', 'created_at', 'processed_at')
    list_filter = ('payment_method', 'status', 'created_at', 'processed_at')
    search_fields = ('user__email', 'transaction_id')
    readonly_fields = ('created_at', 'updated_at')

    def save_model(self, request, obj, form, change):
        if obj.status in {MembershipPayment.PaymentStatus.APPROVED, MembershipPayment.PaymentStatus.REJECTED, MembershipPayment.PaymentStatus.FAILED}:
            if not obj.processed_by:
                obj.processed_by = request.user
            if not obj.processed_at:
                obj.processed_at = timezone.now()
        super().save_model(request, obj, form, change)
