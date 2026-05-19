from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import MembershipPayment
from .forms import PaymentForm
from django.conf import settings


@login_required
def payment_view(request):
    latest_payment = MembershipPayment.objects.filter(user=request.user).first()
    context = {
        'membership_fee': settings.MEMBERSHIP_FEE,
        'jazzcash_account': settings.JAZZCASH_ACCOUNT,
        'easypaisa_account': settings.EASYPAISA_ACCOUNT,
        'payfast_merchant_id': settings.PAYFAST_MERCHANT_ID,
        'payment_receiver_name': settings.PAYMENT_RECEIVER_NAME,
        'latest_payment': latest_payment,
    }
    return render(request, 'dashboard/payment.html', context)


@login_required
def submit_payment(request):
    existing_open = MembershipPayment.objects.filter(
        user=request.user,
        status__in=[
            MembershipPayment.PaymentStatus.PENDING,
            MembershipPayment.PaymentStatus.PROCESSING,
        ]
    ).first()
    if existing_open:
        messages.info(request, 'Aap ki payment verification already pending hai. Admin review ka wait karein.')
        return redirect('payment_history')

    latest_payment = MembershipPayment.objects.filter(user=request.user).first()
    if latest_payment and latest_payment.status in {
        MembershipPayment.PaymentStatus.PENDING,
        MembershipPayment.PaymentStatus.PROCESSING,
        MembershipPayment.PaymentStatus.APPROVED,
    }:
        messages.info(request, 'Aap ki payment request already submitted hai. Status check karein.')
        return redirect('payment_history')

    if request.method == 'POST':
        form = PaymentForm(request.POST, request.FILES)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.user = request.user
            payment.amount = settings.MEMBERSHIP_FEE
            payment.status = MembershipPayment.PaymentStatus.PENDING
            payment.save()
            
            messages.success(request, 'Payment submitted successfully. Please wait for approval.')
            return redirect('payment_history')
    else:
        form = PaymentForm()
    
    return render(request, 'dashboard/submit_payment.html', {
        'form': form,
        'membership_fee': settings.MEMBERSHIP_FEE,
        'jazzcash_account': settings.JAZZCASH_ACCOUNT,
        'easypaisa_account': settings.EASYPAISA_ACCOUNT,
        'payfast_merchant_id': settings.PAYFAST_MERCHANT_ID,
        'payment_receiver_name': settings.PAYMENT_RECEIVER_NAME,
    })


@login_required
def payment_history(request):
    payments = MembershipPayment.objects.filter(user=request.user)
    
    context = {
        'payments': payments,
    }
    return render(request, 'dashboard/payment_history.html', context)
