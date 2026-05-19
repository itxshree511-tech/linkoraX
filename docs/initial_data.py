"""
Run this script in Django shell to initialize levels and achievements:
python manage.py shell < docs/initial_data.py
"""

from levels.models import Level, Achievement

# Create Levels
levels_data = [
    {
        'name': 'Bronze Member',
        'level_number': 1,
        'min_referrals': 0,
        'commission_percentage': 10.00,
        'badge_icon': '🥉',
        'badge_color': '#CD7F32',
        'benefits': 'Access to basic resources, 10% referral commission'
    },
    {
        'name': 'Silver Member',
        'level_number': 2,
        'min_referrals': 20,
        'commission_percentage': 12.00,
        'badge_icon': '🥈',
        'badge_color': '#C0C0C0',
        'benefits': 'Access to premium resources, 12% referral commission'
    },
    {
        'name': 'Gold Member',
        'level_number': 3,
        'min_referrals': 50,
        'commission_percentage': 15.00,
        'badge_icon': '🥇',
        'badge_color': '#FFD700',
        'benefits': 'Access to all resources, 15% referral commission, priority support'
    },
    {
        'name': 'Platinum Member',
        'level_number': 4,
        'min_referrals': 100,
        'commission_percentage': 20.00,
        'badge_icon': '💎',
        'badge_color': '#E5E4E2',
        'benefits': 'VIP access, 20% referral commission, exclusive resources, dedicated support'
    }
]

for level_data in levels_data:
    Level.objects.get_or_create(
        level_number=level_data['level_number'],
        defaults=level_data
    )

# Create Achievements
achievements_data = [
    {
        'name': 'First Referral',
        'slug': 'first-referral',
        'description': 'Refer your first member to the platform',
        'icon': '🎯',
        'points': 10
    },
    {
        'name': 'Rising Star',
        'slug': 'rising-star',
        'description': 'Reach 10 total referrals',
        'icon': '⭐',
        'points': 50
    },
    {
        'name': 'Community Builder',
        'slug': 'community-builder',
        'description': 'Reach 50 total referrals',
        'icon': '🏗️',
        'points': 200
    },
    {
        'name': 'Top Promoter',
        'slug': 'top-promoter',
        'description': 'Reach 100 total referrals',
        'icon': '🚀',
        'points': 500
    },
    {
        'name': 'Level Up',
        'slug': 'level-up',
        'description': 'Reach Level 2',
        'icon': '📈',
        'points': 100
    },
    {
        'name': 'Elite Member',
        'slug': 'elite-member',
        'description': 'Reach Level 3',
        'icon': '👑',
        'points': 300
    },
    {
        'name': 'Legend',
        'slug': 'legend',
        'description': 'Reach Level 4',
        'icon': '🏆',
        'points': 1000
    },
    {
        'name': 'First Withdrawal',
        'slug': 'first-withdrawal',
        'description': 'Complete your first successful withdrawal',
        'icon': '💰',
        'points': 25
    }
]

for achievement_data in achievements_data:
    Achievement.objects.get_or_create(
        slug=achievement_data['slug'],
        defaults=achievement_data
    )

print("Levels and achievements initialized successfully!")
