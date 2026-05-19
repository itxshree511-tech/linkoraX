from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Referral, ReferralStats
from payments.services import user_has_active_membership


@login_required
def referral_team(request):
    referrals = Referral.objects.filter(referrer=request.user).select_related('referred')
    stats, created = ReferralStats.objects.get_or_create(user=request.user)
    can_share_referral = user_has_active_membership(request.user)
    referral_link = f"{request.build_absolute_uri('/register/')}?ref={request.user.referral_code}"
    
    context = {
        'referrals': referrals,
        'stats': stats,
        'can_share_referral': can_share_referral,
        'referral_link': referral_link,
    }
    return render(request, 'dashboard/referral_team.html', context)


@login_required
def referral_link(request):
    if not user_has_active_membership(request.user):
        messages.info(request, 'Referral link unlock karne ke liye pehle membership payment complete karein.')
        return redirect('payment')

    referral_link = f"{request.build_absolute_uri('/register/')}?ref={request.user.referral_code}"
    context = {
        'referral_link': referral_link,
        'referral_code': request.user.referral_code,
    }
    return render(request, 'dashboard/referral_link.html', context)
