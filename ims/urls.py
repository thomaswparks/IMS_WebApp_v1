from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib import admin
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('newitem/', views.newItem, name='newItem'),
    path('updateitem/<int:pk>/', views.updateItem, name='updateItem'),
    path('profile/', include('account.urls'), name="profile"),
]
