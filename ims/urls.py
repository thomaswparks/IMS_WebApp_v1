from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('newitem/', views.newItem, name='newItem'),
    path('updateitem/', views.updateItem, name='updateItem'),
]
