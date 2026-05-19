from django.contrib import admin
from .models import Level, UserLevel, Achievement, UserAchievement


@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):
    list_display = ('level_number', 'name', 'min_referrals', 'commission_percentage')
    ordering = ('level_number',)


@admin.register(UserLevel)
class UserLevelAdmin(admin.ModelAdmin):
    list_display = ('user', 'level', 'total_referrals', 'progress_to_next')
    search_fields = ('user__email',)


@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'points')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(UserAchievement)
class UserAchievementAdmin(admin.ModelAdmin):
    list_display = ('user', 'achievement', 'earned_at')
    search_fields = ('user__email', 'achievement__name')
