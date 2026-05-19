from django.urls import path
from . import views
from .webhooks import payment_webhook

urlpatterns = [
    path('', views.payment_view, name='payment'),
    path('submit/', views.submit_payment, name='submit_payment'),
    path('history/', views.payment_history, name='payment_history'),
    path('webhook/<str:provider>/', payment_webhook, name='payment_webhook'),
]
