from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib import admin
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('newitem/', views.newItem, name='newItem'),
    path('updateitem/<int:pk>/', views.updateItem, name='updateItem'),
    path('delete/<int:pk>/', views.delete_item, name="delete_item"),
    path('new_sub/<int:pk>/', views.new_sub, name="new_sub"),
]
