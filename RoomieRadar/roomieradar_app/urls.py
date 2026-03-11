from django.urls import path
from . import views

urlpatterns = [
    path('', views.room_home, name='room_home'),
    path('hostel-only/', views.hostel_only, name='hostel_only'),
    path('matches/', views.find_matches, name='find_matches'),
    path('book/<int:room_id>/', views.book_bed, name='book_bed'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('ajax/filter-rooms/', views.ajax_filter_rooms, name='ajax_filter_rooms'),
    path('cancel-booking/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
]
