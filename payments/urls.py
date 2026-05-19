from django.urls import path
from . import views

urlpatterns = [
    path('', views.payment_view, name='payment'),
    path('submit/', views.submit_payment, name='submit_payment'),
    path('history/', views.payment_history, name='payment_history'),
]
