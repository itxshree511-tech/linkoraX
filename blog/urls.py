from django.urls import path
from . import views

urlpatterns = [
    path('', views.blog_list, name='blog_list'),
    path('category/<slug:category_slug>/', views.blog_category, name='blog_category'),
    path('<slug:post_slug>/', views.blog_detail, name='blog_detail'),
]
