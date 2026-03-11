from django.contrib import admin
from .models import Room, Booking
@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = (
        'room_number',
        'room_type',
        'total_beds',
        'occupied_beds',
        'gender',
        'ac_type',
        'room_category'
    )
    readonly_fields = ('total_beds',)
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'room',
        'booked_at'
    )
    list_filter = ('booked_at', 'room__room_category', 'room__gender')
    search_fields = ('user__username', 'room__room_number')
    readonly_fields = ('booked_at',)
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('user', 'room')
