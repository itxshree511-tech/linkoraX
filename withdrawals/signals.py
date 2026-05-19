from django.db import transaction
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone
from decimal import Decimal

from notifications.models import Notification
from wallet.models import Transaction, Wallet

from .models import WithdrawRequest


def _d(value):
    return Decimal(str(value))


@receiver(pre_save, sender=WithdrawRequest)
def capture_old_withdraw_status(sender, instance, **kwargs):
    if not instance.pk:
        instance._old_status = None
        return
    old = sender.objects.filter(pk=instance.pk).values_list('status', flat=True).first()
    instance._old_status = old


@receiver(post_save, sender=WithdrawRequest)
def handle_withdraw_status_change(sender, instance, created, **kwargs):
    if created:
        return

    old_status = getattr(instance, '_old_status', None)
    new_status = instance.status
    if old_status == new_status:
        return

    wallet, _ = Wallet.objects.get_or_create(user=instance.user)

    with transaction.atomic():
        if new_status == WithdrawRequest.WithdrawStatus.REJECTED:
            wallet.balance = _d(wallet.balance) + _d(instance.amount)
            wallet.pending_withdrawals = max(_d(wallet.pending_withdrawals) - _d(instance.amount), Decimal('0.00'))
            wallet.save(update_fields=['balance', 'pending_withdrawals', 'updated_at'])
            Transaction.objects.create(
                wallet=wallet,
                transaction_type=Transaction.TransactionType.CREDIT,
                amount=instance.amount,
                status=Transaction.TransactionStatus.COMPLETED,
                description='Withdrawal rejected: amount returned to wallet',
                reference_id=str(instance.id),
            )
            Notification.objects.create(
                user=instance.user,
                title='Withdrawal Rejected',
                message='Your withdrawal request was rejected and funds were returned to your wallet.',
                notification_type=Notification.NotificationType.WARNING,
            )

        elif new_status == WithdrawRequest.WithdrawStatus.PAID:
            wallet.pending_withdrawals = max(_d(wallet.pending_withdrawals) - _d(instance.amount), Decimal('0.00'))
            wallet.total_withdrawn = _d(wallet.total_withdrawn) + _d(instance.amount)
            wallet.save(update_fields=['pending_withdrawals', 'total_withdrawn', 'updated_at'])
            Transaction.objects.create(
                wallet=wallet,
                transaction_type=Transaction.TransactionType.DEBIT,
                amount=instance.amount,
                status=Transaction.TransactionStatus.COMPLETED,
                description='Withdrawal paid successfully',
                reference_id=str(instance.id),
            )
            Notification.objects.create(
                user=instance.user,
                title='Withdrawal Paid',
                message='Your withdrawal has been processed successfully.',
                notification_type=Notification.NotificationType.SUCCESS,
            )

    if new_status in {WithdrawRequest.WithdrawStatus.REJECTED, WithdrawRequest.WithdrawStatus.PAID} and instance.processed_at is None:
        WithdrawRequest.objects.filter(pk=instance.pk).update(processed_at=timezone.now())
