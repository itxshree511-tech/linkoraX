from django.urls import path
from . import views

urlpatterns = [
    path('', views.withdraw_view, name='withdraw'),
    path('request/', views.request_withdrawal, name='request_withdrawal'),
    path('history/', views.withdraw_history, name='withdraw_history'),
]
