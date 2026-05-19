from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, UserProfile


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'


class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('email', 'role', 'account_status', 'email_verified', 'phone_verified', 'created_at')
    list_filter = ('role', 'account_status', 'email_verified', 'phone_verified', 'created_at')
    search_fields = ('email', 'referral_code', 'phone')
    ordering = ('-created_at',)
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('phone', 'avatar')}),
        ('Account Status', {'fields': ('role', 'account_status', 'email_verified', 'phone_verified')}),
        ('Referral Info', {'fields': ('referral_code',)}),
        ('Security', {'fields': ('ip_address', 'user_agent')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'last_activity', 'created_at', 'updated_at')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'role'),
        }),
    )


admin.site.register(User, UserAdmin)
admin.site.register(UserProfile)
