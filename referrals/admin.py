from django.contrib import admin
from .models import Referral, ReferralStats


@admin.register(Referral)
class ReferralAdmin(admin.ModelAdmin):
    list_display = ('referrer', 'referred', 'level', 'commission_amount', 'commission_paid', 'is_suspicious', 'created_at')
    list_filter = ('level', 'commission_paid', 'is_suspicious', 'created_at')
    search_fields = ('referrer__email', 'referred__email')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(ReferralStats)
class ReferralStatsAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_referrals', 'level_1_count', 'level_2_count', 'total_commissions', 'active_referrals')
    search_fields = ('user__email',)
    readonly_fields = ('created_at', 'updated_at')
