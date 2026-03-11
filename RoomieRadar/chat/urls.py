from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat_home, name='chat_home'),
    path('start/<int:user_id>/', views.start_chat, name='start_chat'),
    path('room/<int:room_id>/', views.chat_room, name='chat_room'),
    path('block/<int:user_id>/', views.block_user, name='block_user'),
    path('unblock/<int:user_id>/', views.unblock_user, name='unblock_user'),
    path('report/<int:user_id>/', views.report_user, name='report_user'),
    path('download/<int:message_id>/', views.download_file, name='download_file'),
]
