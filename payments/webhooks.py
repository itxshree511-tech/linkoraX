import hashlib
import hmac
import json
from decimal import Decimal, InvalidOperation

from django.conf import settings
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .models import MembershipPayment


def _provider_secret(provider):
    if provider == MembershipPayment.PaymentMethod.JAZZCASH:
        return (settings.JAZZCASH_WEBHOOK_SECRET or '').strip()
    if provider == MembershipPayment.PaymentMethod.EASYPAISA:
        return (settings.EASYPAISA_WEBHOOK_SECRET or '').strip()
    return ''


def _provider_account(provider):
    if provider == MembershipPayment.PaymentMethod.JAZZCASH:
        return (settings.JAZZCASH_ACCOUNT or '').strip()
    if provider == MembershipPayment.PaymentMethod.EASYPAISA:
        return (settings.EASYPAISA_ACCOUNT or '').strip()
    return ''


def _valid_signature(provider, body, signature):
    secret = _provider_secret(provider)
    if not secret:
        return False
    expected = hmac.new(secret.encode('utf-8'), body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, (signature or '').strip())


def _normalize_status(value):
    raw = str(value or '').strip().lower()
    if raw in {'success', 'successful', 'completed', 'approved', 'paid'}:
        return MembershipPayment.PaymentStatus.APPROVED
    if raw in {'failed', 'failure', 'error'}:
        return MembershipPayment.PaymentStatus.FAILED
    if raw in {'pending', 'processing', 'in_process'}:
        return MembershipPayment.PaymentStatus.PROCESSING
    return ''


def _decimal(value):
    try:
        return Decimal(str(value))
    except (InvalidOperation, TypeError, ValueError):
        return None


@csrf_exempt
@require_POST
def payment_webhook(request, provider):
    provider = (provider or '').strip().lower()
    if provider not in {
        MembershipPayment.PaymentMethod.JAZZCASH,
        MembershipPayment.PaymentMethod.EASYPAISA,
    }:
        return JsonResponse({'ok': False, 'error': 'Unsupported provider'}, status=404)

    signature = request.headers.get('X-Payment-Signature') or request.headers.get('X-Signature')
    if not _valid_signature(provider, request.body, signature):
        return JsonResponse({'ok': False, 'error': 'Invalid signature'}, status=401)

    try:
        payload = json.loads(request.body.decode('utf-8'))
    except (UnicodeDecodeError, json.JSONDecodeError):
        return JsonResponse({'ok': False, 'error': 'Invalid JSON payload'}, status=400)

    transaction_id = str(payload.get('transaction_id') or payload.get('txn_id') or '').strip()
    status = _normalize_status(payload.get('status'))
    sender_amount = _decimal(payload.get('amount'))
    receiver_account = str(payload.get('receiver_account') or payload.get('account') or '').strip()

    if not transaction_id:
        return JsonResponse({'ok': False, 'error': 'transaction_id is required'}, status=400)
    if not status:
        return JsonResponse({'ok': False, 'error': 'Unsupported payment status'}, status=400)

    payment = (
        MembershipPayment.objects.select_related('user')
        .filter(transaction_id__iexact=transaction_id, payment_method=provider)
        .first()
    )
    if not payment:
        return JsonResponse({'ok': False, 'error': 'Payment request not found'}, status=404)

    expected_account = _provider_account(provider)
    if expected_account and receiver_account and expected_account != receiver_account:
        payment.status = MembershipPayment.PaymentStatus.FAILED
        payment.admin_notes = (
            f'Webhook receiver mismatch. Expected {expected_account}, got {receiver_account}. '
            f'[{timezone.now().isoformat()}]'
        )
        payment.save(update_fields=['status', 'admin_notes', 'updated_at'])
        return JsonResponse({'ok': False, 'error': 'Receiver account mismatch'}, status=400)

    if sender_amount is not None and sender_amount != payment.amount:
        payment.status = MembershipPayment.PaymentStatus.PROCESSING
        payment.admin_notes = (
            f'Webhook amount mismatch. Expected {payment.amount}, got {sender_amount}. '
            f'[{timezone.now().isoformat()}]'
        )
        payment.save(update_fields=['status', 'admin_notes', 'updated_at'])
        return JsonResponse({'ok': True, 'status': 'processing', 'reason': 'amount_mismatch'}, status=202)

    payment.status = status
    if status in {
        MembershipPayment.PaymentStatus.APPROVED,
        MembershipPayment.PaymentStatus.FAILED,
        MembershipPayment.PaymentStatus.REJECTED,
    } and payment.processed_at is None:
        payment.processed_at = timezone.now()

    primary_admin = (
        get_user_model()
        .objects.filter(email__iexact=getattr(settings, 'PRIMARY_ADMIN_EMAIL', ''))
        .first()
    )
    if primary_admin and payment.processed_by_id is None:
        payment.processed_by = primary_admin

    note = f'Webhook ({provider}) updated status to {status}. [{timezone.now().isoformat()}]'
    payment.admin_notes = f'{payment.admin_notes}\n{note}'.strip() if payment.admin_notes else note
    payment.save(update_fields=['status', 'processed_at', 'processed_by', 'admin_notes', 'updated_at'])

    return JsonResponse({'ok': True, 'status': status, 'payment_id': str(payment.id)})
