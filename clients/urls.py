from django.urls import path

from . import views

urlpatterns = [
    path('', views.clients_list, name='client_list'),
    path('ping/', views.health_check, name='client_ping'),
    path('create/', views.client_create, name='client_create'),
    path('<int:pk>/update/', views.client_update, name='client_update'),
    path('<int:pk>/delete/', views.client_delete, name='client_delete'),
]
