from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('activate/', views.activate_account, name='activate'),
    path('logout/', views.logout_view, name='logout'),
]
