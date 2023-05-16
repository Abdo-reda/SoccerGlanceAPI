
from django.urls import path
from . import views

urlpatterns = [
    path('start_match/', views.start_match),
    path('end_match/', views.end_match),
    path('add_highlight/', views.add_highlight),
    path('register_user/', views.register_user_view),
    path('login_user/', views.login_user_view),
    path('logout_user/', views.logout_user_view),

    path('get_latest_highlight/', views.get_latest_highlight),
    path('get_all_highlights/', views.get_all_highlights),
    path('get_all_live_premium_matches/', views.get_all_live_premium_matches),
    path('get_all_future_premium_matches/',
         views.get_all_future_premium_matches),
    path('get_premium_matches_happening_today/',
         views.get_premium_matches_happening_today),
    
    path('get_all_live_custom_matches/', views.get_all_live_custom_matches),
    path('get_all_future_custom_matches/',
         views.get_all_future_custom_matches),
    path('get_custom_matches_happening_today/',
         views.get_custom_matches_happening_today),

    path('get_match_info/', views.get_match_info),
    path('register_for_match/', views.register_for_match),
    path('hamadaForTeamSpirit/', views.hamadaForTeamSpirit),


]


'''
TODO:

- Design
  - Fix the Pricing

- Add more endpoints
 - Full match processing at once (offline custom matches)

- Demo video
  - Record demo of overall project
  - Record demo of highlights generation
  - Add Demo part in navbar 

'''
