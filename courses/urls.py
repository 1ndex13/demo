#Личный кабинет и заявки(маршруты)
from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    path('cabinet/', views.cabinet_view, name='cabinet'),
    path('apply/', views.apply_view, name='apply'),
    path('review/add/', views.add_review_view, name='add_review'),
]
