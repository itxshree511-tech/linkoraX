from django.contrib import admin
from .models import FraudLog, SuspiciousIP


@admin.register(FraudLog)
class FraudLogAdmin(admin.ModelAdmin):
    list_display = ('fraud_type', 'user', 'severity', 'is_resolved', 'created_at')
    list_filter = ('fraud_type', 'severity', 'is_resolved', 'created_at')
    search_fields = ('user__email', 'description')


@admin.register(SuspiciousIP)
class SuspiciousIPAdmin(admin.ModelAdmin):
    list_display = ('ip_address', 'attempt_count', 'is_blocked', 'created_at')
    list_filter = ('is_blocked', 'created_at')
    search_fields = ('ip_address',)
