from django.urls import path
from . import views

urlpatterns = [
    path('app/', views.app_home, name='app_home'),
    path('with-roommate/', views.with_roommate, name='with_roommate'),
    path('profile/', views.profile_view, name='profile'),
path('profile/<int:user_id>/', views.view_user_profile, name='view_profile'),
    path('preferences/', views.preferences_view, name='preferences'),
]
