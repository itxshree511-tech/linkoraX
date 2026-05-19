from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import WithdrawRequest
from .forms import WithdrawRequestForm
from django.conf import settings
from wallet.models import Wallet
from payments.services import user_has_active_membership
from decimal import Decimal


@login_required
def withdraw_view(request):
    wallet, created = Wallet.objects.get_or_create(user=request.user)
    withdraw_history = WithdrawRequest.objects.filter(user=request.user)
    
    context = {
        'wallet': wallet,
        'withdraw_history': withdraw_history,
        'minimum_withdrawal': settings.MINIMUM_WITHDRAWAL,
    }
    return render(request, 'dashboard/withdraw.html', context)


@login_required
def request_withdrawal(request):
    wallet, created = Wallet.objects.get_or_create(user=request.user)

    if not request.user.email_verified:
        messages.error(request, 'Email verification is required before withdrawal.')
        return redirect('withdraw')

    if request.user.account_status != 'active':
        messages.error(request, 'Your account is not eligible for withdrawal right now.')
        return redirect('withdraw')

    if wallet.is_frozen:
        messages.error(request, 'Your wallet is currently frozen. Please contact support.')
        return redirect('withdraw')

    if not user_has_active_membership(request.user):
        messages.error(request, 'Active membership is required before withdrawal.')
        return redirect('withdraw')
    
    if wallet.balance < settings.MINIMUM_WITHDRAWAL:
        messages.error(request, f'You need at least {settings.MINIMUM_WITHDRAWAL} PKR to request a withdrawal.')
        return redirect('withdraw')
    
    if request.method == 'POST':
        form = WithdrawRequestForm(request.POST)
        if form.is_valid():
            withdrawal = form.save(commit=False)
            withdrawal.user = request.user
            
            if withdrawal.amount > wallet.balance:
                messages.error(request, 'Insufficient wallet balance.')
                return redirect('request_withdrawal')
            
            withdrawal.save()
            
            # Deduct from wallet
            wallet.balance = Decimal(str(wallet.balance)) - Decimal(str(withdrawal.amount))
            wallet.pending_withdrawals = Decimal(str(wallet.pending_withdrawals)) + Decimal(str(withdrawal.amount))
            wallet.save()
            
            messages.success(request, 'Withdrawal request submitted successfully.')
            return redirect('withdraw_history')
    else:
        form = WithdrawRequestForm()
    
    context = {
        'form': form,
        'wallet': wallet,
        'minimum_withdrawal': settings.MINIMUM_WITHDRAWAL,
    }
    return render(request, 'dashboard/request_withdrawal.html', context)


@login_required
def withdraw_history(request):
    withdrawals = WithdrawRequest.objects.filter(user=request.user)
    
    context = {
        'withdrawals': withdrawals,
    }
    return render(request, 'dashboard/withdraw_history.html', context)
