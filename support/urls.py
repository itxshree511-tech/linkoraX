from django.urls import path
from . import views

urlpatterns = [
    path('', views.support_view, name='support'),
    path('create/', views.create_ticket, name='create_ticket'),
    path('ticket/<uuid:ticket_id>/', views.ticket_detail, name='ticket_detail'),
]
