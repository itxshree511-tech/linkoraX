from django.db import models
from django.conf import settings
import uuid


class Level(models.Model):
    name = models.CharField(max_length=100)
    level_number = models.IntegerField(unique=True)
    min_referrals = models.IntegerField(default=0)
    commission_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=10.00)
    
    badge_icon = models.CharField(max_length=200, blank=True, null=True)
    badge_color = models.CharField(max_length=20, default='#3B82F6')
    
    benefits = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'levels'
        verbose_name = 'Level'
        verbose_name_plural = 'Levels'
        ordering = ['level_number']
    
    def __str__(self):
        return f"Level {self.level_number} - {self.name}"


class UserLevel(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_level')
    level = models.ForeignKey(Level, on_delete=models.PROTECT, related_name='user_levels')
    
    total_referrals = models.IntegerField(default=0)
    progress_to_next = models.IntegerField(default=0)
    
    achievements = models.JSONField(default=list, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'user_levels'
        verbose_name = 'User Level'
        verbose_name_plural = 'User Levels'
    
    def __str__(self):
        return f"{self.user.email} - {self.level.name}"


class Achievement(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField()
    
    icon = models.CharField(max_length=200, blank=True, null=True)
    points = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'achievements'
        verbose_name = 'Achievement'
        verbose_name_plural = 'Achievements'
    
    def __str__(self):
        return self.name


class UserAchievement(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='achievements')
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE, related_name='user_achievements')
    
    earned_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'user_achievements'
        verbose_name = 'User Achievement'
        verbose_name_plural = 'User Achievements'
        unique_together = ['user', 'achievement']
    
    def __str__(self):
        return f"{self.user.email} - {self.achievement.name}"
