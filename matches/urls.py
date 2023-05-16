from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('create_match/', views.create_match, name='create_match'),
]


