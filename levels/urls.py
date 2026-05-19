from django.urls import path
from . import views

urlpatterns = [
    path('', views.levels_view, name='levels'),
    path('achievements/', views.achievements_view, name='achievements'),
]
