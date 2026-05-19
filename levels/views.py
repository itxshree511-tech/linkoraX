from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Level, UserLevel, Achievement, UserAchievement


def get_or_create_user_level(user):
    base_level = Level.objects.order_by('level_number').first()
    if not base_level:
        base_level = Level.objects.create(
            name='Starter',
            level_number=1,
            min_referrals=0,
            commission_percentage=10.00,
        )
    user_level, _ = UserLevel.objects.get_or_create(user=user, defaults={'level': base_level})
    return user_level


@login_required
def levels_view(request):
    user_level = get_or_create_user_level(request.user)
    all_levels = Level.objects.all()
    user_achievements = UserAchievement.objects.filter(user=request.user)
    
    context = {
        'user_level': user_level,
        'all_levels': all_levels,
        'user_achievements': user_achievements,
    }
    return render(request, 'dashboard/levels.html', context)


@login_required
def achievements_view(request):
    get_or_create_user_level(request.user)
    user_achievements = UserAchievement.objects.filter(user=request.user).select_related('achievement')
    all_achievements = Achievement.objects.all()
    
    context = {
        'user_achievements': user_achievements,
        'all_achievements': all_achievements,
    }
    return render(request, 'dashboard/achievements.html', context)
