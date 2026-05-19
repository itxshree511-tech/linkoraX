from django.urls import path
from . import views

urlpatterns = [
    path('', views.resources_view, name='resources'),
    path('category/<slug:category_slug>/', views.resources_by_category, name='resources_by_category'),
    path('<slug:resource_slug>/', views.resource_detail, name='resource_detail'),
]
