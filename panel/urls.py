#URL-маршруты панели администратора
from django.urls import path
from . import views

app_name = 'panel'

urlpatterns = [
    path('', views.panel_index, name='index'),
    path('status/<int:app_id>/', views.change_status, name='change_status'),
]
