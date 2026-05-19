from django.urls import path
from . import views

urlpatterns = [
    path('', views.referral_team, name='referral_team'),
    path('link/', views.referral_link, name='referral_link'),
]
