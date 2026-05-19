from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from .models import MembershipPayment
from .services import process_payment_approval


@receiver(pre_save, sender=MembershipPayment)
def capture_old_payment_status(sender, instance, **kwargs):
    if not instance.pk:
        instance._old_status = None
        return
    old = sender.objects.filter(pk=instance.pk).values_list('status', flat=True).first()
    instance._old_status = old


@receiver(post_save, sender=MembershipPayment)
def handle_payment_status_change(sender, instance, created, **kwargs):
    old_status = getattr(instance, '_old_status', None)
    if instance.status == MembershipPayment.PaymentStatus.APPROVED and old_status != MembershipPayment.PaymentStatus.APPROVED:
        process_payment_approval(instance)

