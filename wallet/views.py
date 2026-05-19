from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Wallet, Transaction


@login_required
def wallet_view(request):
    wallet, created = Wallet.objects.get_or_create(user=request.user)
    recent_transactions = wallet.transactions.all()[:10]
    
    context = {
        'wallet': wallet,
        'recent_transactions': recent_transactions,
    }
    return render(request, 'dashboard/wallet.html', context)


@login_required
def transactions(request):
    wallet, created = Wallet.objects.get_or_create(user=request.user)
    transactions = wallet.transactions.all()
    
    context = {
        'transactions': transactions,
    }
    return render(request, 'dashboard/transactions.html', context)


@login_required
def earnings(request):
    wallet, created = Wallet.objects.get_or_create(user=request.user)
    
    context = {
        'wallet': wallet,
    }
    return render(request, 'dashboard/earnings.html', context)
