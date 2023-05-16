

from django.urls import path
from . import views


urlpatterns = [

    path('custom_matches/', views.custom_matches_dashboard,
         name='custom_matches_dashboard'),
    path('premium_matches/', views.premium_matches_dashboard,
         name='premium_matches_dashboard'),

]
