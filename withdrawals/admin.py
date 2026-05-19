from django.contrib import admin
from django import forms
from django.utils import timezone
from .models import WithdrawRequest


class WithdrawRequestAdminForm(forms.ModelForm):
    class Meta:
        model = WithdrawRequest
        fields = '__all__'

    def clean(self):
        cleaned = super().clean()
        status = cleaned.get('status')
        admin_notes = (cleaned.get('admin_notes') or '').strip()
        if status in {
            WithdrawRequest.WithdrawStatus.APPROVED,
            WithdrawRequest.WithdrawStatus.REJECTED,
            WithdrawRequest.WithdrawStatus.PAID,
        } and not admin_notes:
            raise forms.ValidationError('Admin notes are required when approving/rejecting/marking paid.')
        return cleaned


@admin.register(WithdrawRequest)
class WithdrawRequestAdmin(admin.ModelAdmin):
    form = WithdrawRequestAdminForm
    list_display = ('user', 'amount', 'withdraw_method', 'account_number', 'status', 'created_at', 'processed_at')
    list_filter = ('withdraw_method', 'status', 'created_at', 'processed_at')
    search_fields = ('user__email', 'account_number')
    readonly_fields = ('created_at', 'updated_at')

    def save_model(self, request, obj, form, change):
        if obj.status in {WithdrawRequest.WithdrawStatus.APPROVED, WithdrawRequest.WithdrawStatus.REJECTED, WithdrawRequest.WithdrawStatus.PAID}:
            if not obj.processed_by:
                obj.processed_by = request.user
            if not obj.processed_at:
                obj.processed_at = timezone.now()
        super().save_model(request, obj, form, change)
