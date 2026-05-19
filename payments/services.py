from decimal import Decimal

from django.conf import settings
from django.db import transaction
from django.utils import timezone

from levels.models import Level, UserLevel
from notifications.models import Notification
from referrals.models import Referral, ReferralStats
from wallet.models import Transaction, Wallet


def user_has_active_membership(user):
    return user.payments.filter(status='approved').exists()


def _d(value):
    return Decimal(str(value))


def _get_or_create_base_level():
    level = Level.objects.order_by('level_number').first()
    if level:
        return level
    return Level.objects.create(
        name='Starter',
        level_number=1,
        min_referrals=0,
        commission_percentage=Decimal('10.00'),
    )


def _refresh_user_level(user, direct_active_referrals):
    base = _get_or_create_base_level()
    target = (
        Level.objects.filter(min_referrals__lte=direct_active_referrals)
        .order_by('-min_referrals', '-level_number')
        .first()
        or base
    )
    user_level, _ = UserLevel.objects.get_or_create(user=user, defaults={'level': base})
    user_level.level = target
    user_level.total_referrals = direct_active_referrals
    user_level.save(update_fields=['level', 'total_referrals', 'updated_at'])


@transaction.atomic
def process_payment_approval(payment):
    if payment.status != 'approved':
        return

    user = payment.user
    if payment.processed_at is None:
        payment.processed_at = timezone.now()
        payment.save(update_fields=['processed_at', 'updated_at'])

    Notification.objects.create(
        user=user,
        title='Membership Activated',
        message='Your membership payment has been approved successfully.',
        notification_type=Notification.NotificationType.SUCCESS,
    )

    direct_ref = Referral.objects.select_related('referrer', 'referred').filter(referred=user).first()
    if not direct_ref or direct_ref.commission_paid:
        return

    membership_fee = _d(payment.amount)
    level1_pct = Decimal(str(getattr(settings, 'REFERRAL_LEVEL_1_COMMISSION', 10)))
    level2_pct = Decimal(str(getattr(settings, 'REFERRAL_LEVEL_2_COMMISSION', 10)))
    level1_commission = (membership_fee * level1_pct) / Decimal('100')
    level2_commission = (level1_commission * level2_pct) / Decimal('100')

    level1_wallet, _ = Wallet.objects.get_or_create(user=direct_ref.referrer)
    level1_wallet.balance = _d(level1_wallet.balance) + level1_commission
    level1_wallet.total_earnings = _d(level1_wallet.total_earnings) + level1_commission
    level1_wallet.referral_earnings = _d(level1_wallet.referral_earnings) + level1_commission
    level1_wallet.save(update_fields=['balance', 'total_earnings', 'referral_earnings', 'updated_at'])
    Transaction.objects.create(
        wallet=level1_wallet,
        transaction_type=Transaction.TransactionType.CREDIT,
        amount=level1_commission,
        status=Transaction.TransactionStatus.COMPLETED,
        description=f'Direct referral reward from {user.email}',
        reference_id=str(payment.id),
    )

    level1_stats, _ = ReferralStats.objects.get_or_create(user=direct_ref.referrer)
    level1_stats.total_referrals += 1
    level1_stats.level_1_count += 1
    level1_stats.active_referrals += 1
    level1_stats.total_commissions = _d(level1_stats.total_commissions) + level1_commission
    level1_stats.level_1_commissions = _d(level1_stats.level_1_commissions) + level1_commission
    level1_stats.save()
    _refresh_user_level(direct_ref.referrer, level1_stats.active_referrals)

    Notification.objects.create(
        user=direct_ref.referrer,
        title='New Referral Reward',
        message=f'You received {level1_commission} PKR as direct referral reward.',
        notification_type=Notification.NotificationType.SUCCESS,
    )

    uplink = Referral.objects.select_related('referrer').filter(referred=direct_ref.referrer).first()
    if uplink:
        level2_wallet, _ = Wallet.objects.get_or_create(user=uplink.referrer)
        level2_wallet.balance = _d(level2_wallet.balance) + level2_commission
        level2_wallet.total_earnings = _d(level2_wallet.total_earnings) + level2_commission
        level2_wallet.team_commissions = _d(level2_wallet.team_commissions) + level2_commission
        level2_wallet.save(update_fields=['balance', 'total_earnings', 'team_commissions', 'updated_at'])
        Transaction.objects.create(
            wallet=level2_wallet,
            transaction_type=Transaction.TransactionType.CREDIT,
            amount=level2_commission,
            status=Transaction.TransactionStatus.COMPLETED,
            description=f'Level 2 team commission from {user.email}',
            reference_id=str(payment.id),
        )
        level2_stats, _ = ReferralStats.objects.get_or_create(user=uplink.referrer)
        level2_stats.total_referrals += 1
        level2_stats.level_2_count += 1
        level2_stats.total_commissions = _d(level2_stats.total_commissions) + level2_commission
        level2_stats.level_2_commissions = _d(level2_stats.level_2_commissions) + level2_commission
        level2_stats.save()
        Notification.objects.create(
            user=uplink.referrer,
            title='Team Commission Received',
            message=f'You received {level2_commission} PKR as level 2 team commission.',
            notification_type=Notification.NotificationType.INFO,
        )

    direct_ref.commission_amount = level1_commission
    direct_ref.commission_paid = True
    direct_ref.save(update_fields=['commission_amount', 'commission_paid', 'updated_at'])
