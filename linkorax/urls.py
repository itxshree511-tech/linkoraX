"""
URL configuration for LinkoraX project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.shortcuts import redirect


def single_admin_only(request):
    user = request.user
    if not user.is_authenticated:
        return False
    return (
        user.is_active
        and user.is_staff
        and user.is_superuser
        and user.email
        and user.email.strip().lower() == settings.PRIMARY_ADMIN_EMAIL
    )


admin.site.has_permission = single_admin_only

urlpatterns = [
    path('register/admin', lambda request: redirect('/admin/', permanent=False)),
    path('admin/', admin.site.urls),
    path('', include('users.urls')),
    path('referrals/', include('referrals.urls')),
    path('wallet/', include('wallet.urls')),
    path('payments/', include('payments.urls')),
    path('withdrawals/', include('withdrawals.urls')),
    path('levels/', include('levels.urls')),
    path('resources/', include('resources.urls')),
    path('blog/', include('blog.urls')),
    path('support/', include('support.urls')),
    path('notifications/', include('notifications.urls')),
    path('fraud/', include('fraud.urls')),
    
    # Django REST Auth
    path('api/auth/', include('dj_rest_auth.urls')),
    path('api/auth/registration/', include('dj_rest_auth.registration.urls')),
    
    # Django Allauth
    path('accounts/', include('allauth.urls')),
    
    # CKEditor
    path('ckeditor/', include('ckeditor_uploader.urls')),
    
    # Robots.txt and Sitemap
    path('robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
