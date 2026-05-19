from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_str
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings
from .models import User, UserProfile
from .forms import UserRegistrationForm, UserLoginForm, UserProfileForm
from wallet.models import Wallet
from referrals.models import ReferralStats
from levels.models import Level, UserLevel
from referrals.models import Referral
from fraud.models import FraudLog
from payments.services import user_has_active_membership


def home(request):
    return render(request, 'home.html')


def register(request):
    referral_code = request.POST.get('referral_code') or request.GET.get('ref')

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True
            user.email_verified = True
            user.account_status = 'active'
            user.save()

            if referral_code:
                referrer = User.objects.filter(referral_code=referral_code).first()
                if referrer and referrer.id != user.id:
                    Referral.objects.get_or_create(
                        referred=user,
                        defaults={
                            'referrer': referrer,
                            'level': Referral.ReferralLevel.LEVEL_1,
                            'ip_address': get_client_ip(request),
                            'user_agent': request.META.get('HTTP_USER_AGENT', ''),
                        },
                    )
                elif referrer and referrer.id == user.id:
                    FraudLog.objects.create(
                        user=user,
                        fraud_type=FraudLog.FraudType.SELF_REFERRAL,
                        description='Self-referral blocked during registration.',
                        ip_address=get_client_ip(request),
                        user_agent=request.META.get('HTTP_USER_AGENT', ''),
                        severity='medium',
                    )
            
            messages.success(request, 'Registration successful! You can now login.')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'register.html', {'form': form, 'referral_code': referral_code})


def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email'].strip().lower()
            password = form.cleaned_data['password']

            existing_user = User.objects.filter(email__iexact=email).first()
            # Backward compatibility: old accounts may still be pending verification
            # even though verification is no longer required.
            if existing_user and not existing_user.is_active and existing_user.account_status == 'pending_verification':
                existing_user.is_active = True
                existing_user.email_verified = True
                existing_user.account_status = 'active'
                existing_user.save(update_fields=['is_active', 'email_verified', 'account_status', 'updated_at'])
            
            from django.contrib.auth import authenticate
            user = authenticate(request, email=email, password=password)
            
            if user:
                if user.account_status == 'suspended':
                    messages.error(request, 'Your account has been suspended. Please contact support.')
                    return redirect('login')
                
                if user.account_status == 'frozen':
                    messages.error(request, 'Your account has been frozen. Please contact support.')
                    return redirect('login')
                
                login(request, user)
                
                # Update IP and user agent
                user.ip_address = get_client_ip(request)
                user.user_agent = request.META.get('HTTP_USER_AGENT', '')
                user.save()
                
                messages.success(request, 'Welcome back!')
                return redirect('dashboard')
            else:
                messages.error(request, 'Invalid email or password.')
    else:
        form = UserLoginForm()
    
    return render(request, 'login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            send_password_reset_email(request, user)
            messages.success(request, 'Password reset link has been sent to your email.')
            return redirect('login')
        except User.DoesNotExist:
            messages.error(request, 'No account found with this email.')
    
    return render(request, 'forgot_password.html')


def reset_password(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        
        if default_token_generator.check_token(user, token):
            if request.method == 'POST':
                new_password = request.POST.get('new_password')
                confirm_password = request.POST.get('confirm_password')
                
                if new_password == confirm_password:
                    user.set_password(new_password)
                    user.save()
                    messages.success(request, 'Password has been reset successfully.')
                    return redirect('login')
                else:
                    messages.error(request, 'Passwords do not match.')
            
            return render(request, 'reset_password.html')
        else:
            messages.error(request, 'Invalid or expired reset link.')
            return redirect('forgot_password')
    except:
        messages.error(request, 'Invalid reset link.')
        return redirect('forgot_password')


def verify_email(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        
        if default_token_generator.check_token(user, token):
            user.email_verified = True
            user.is_active = True
            user.account_status = 'active'
            user.save()
            messages.success(request, 'Email verified successfully! You can now login.')
            return redirect('login')
        else:
            messages.error(request, 'Invalid or expired verification link.')
            return redirect('register')
    except:
        messages.error(request, 'Invalid verification link.')
        return redirect('register')


def resend_verification(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            if user.email_verified:
                messages.info(request, 'Your email is already verified.')
            else:
                send_verification_email(request, user)
                messages.success(request, 'Verification email has been sent again.')
        except User.DoesNotExist:
            messages.error(request, 'No account found with this email.')
    
    return render(request, 'resend_verification.html')


@login_required
def dashboard(request):
    wallet, _ = Wallet.objects.get_or_create(user=request.user)
    referral_stats, _ = ReferralStats.objects.get_or_create(user=request.user)
    base_level = Level.objects.order_by('level_number').first()
    if not base_level:
        base_level = Level.objects.create(
            name='Starter',
            level_number=1,
            min_referrals=0,
            commission_percentage=10.00,
        )
    user_level, _ = UserLevel.objects.get_or_create(user=request.user, defaults={'level': base_level})
    recent_transactions = wallet.transactions.all()[:8]

    next_level = Level.objects.filter(level_number__gt=user_level.level.level_number).order_by('level_number').first()
    if next_level:
        next_level_min = next_level.min_referrals
        next_level_name = next_level.name
        next_level_commission = next_level.commission_percentage
        denom = max(next_level_min, 1)
        level_progress = min(100, int((user_level.total_referrals / denom) * 100))
    else:
        next_level_min = user_level.total_referrals
        next_level_name = user_level.level.name
        next_level_commission = user_level.level.commission_percentage
        level_progress = 100

    can_share_referral = user_has_active_membership(request.user)
    referral_link = f"{request.build_absolute_uri('/register/')}?ref={request.user.referral_code}"

    context = {
        'wallet': wallet,
        'referral_stats': referral_stats,
        'user_level': user_level,
        'recent_transactions': recent_transactions,
        'next_level_min': next_level_min,
        'next_level_name': next_level_name,
        'next_level_commission': next_level_commission,
        'level_progress': level_progress,
        'can_share_referral': can_share_referral,
        'referral_link': referral_link,
    }
    return render(request, 'dashboard/dashboard.html', context)


@login_required
def profile(request):
    return render(request, 'dashboard/profile.html')


@login_required
def edit_profile(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=profile, user=request.user)
    
    return render(request, 'dashboard/edit_profile.html', {'form': form})


def about(request):
    return render(request, 'about.html')


def contact(request):
    return render(request, 'contact.html')


def faq(request):
    return render(request, 'faq.html')


def privacy_policy(request):
    return render(request, 'privacy_policy.html')


def terms(request):
    return render(request, 'terms.html')


def disclaimer(request):
    return render(request, 'disclaimer.html')


def refund_policy(request):
    return render(request, 'refund_policy.html')


# Helper functions
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def send_verification_email(request, user):
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    
    verification_url = request.build_absolute_uri(f'/verify-email/{uid}/{token}/')
    
    subject = 'Verify Your Email - LinkoraX'
    message = render_to_string('emails/verify_email.html', {
        'user': user,
        'verification_url': verification_url,
    })
    
    send_mail(
        subject,
        '',
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        html_message=message,
    )


def send_password_reset_email(request, user):
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    
    reset_url = request.build_absolute_uri(f'/reset-password/{uid}/{token}/')
    
    subject = 'Reset Your Password - LinkoraX'
    message = render_to_string('emails/reset_password.html', {
        'user': user,
        'reset_url': reset_url,
    })
    
    send_mail(
        subject,
        '',
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        html_message=message,
    )
