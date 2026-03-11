from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import F

from base.models import Preferences
from .models import Room, Booking
from base.models import Profile

# =================================================
# ROOM MODULE HOME
# =================================================
def room_home(request):
    return HttpResponse("Room & Booking Module")


# =================================================
from django.db.models import F
from base.models import Preferences, Profile
from .models import Room, Booking

from django.utils import timezone
from datetime import timedelta
from django.db.models import F
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from base.models import Preferences, Profile
from .models import Room, Booking

@login_required
@login_required
def find_matches(request):
    # ✅ CHECK: User can only book 1 bed total
    existing_booking = Booking.objects.filter(user=request.user).first()
    if existing_booking:
        messages.info(request, f"You already have a booking in Room {existing_booking.room.room_number}. You can view your booking details below.")
        return redirect('my_bookings')

    try:
        user_pref = Preferences.objects.get(user=request.user)
    except Preferences.DoesNotExist:
        return render(request, 'roomieradar_app/matches.html', {
            'error': 'Please set your preferences first.',
            'preferences_url': True
        })

    matches = []

    # 🔹 Only users who ALREADY BOOKED a roommate room
    bookings = Booking.objects.select_related('user', 'room').filter(
        room__room_category='ROOMMATE',
        room__gender=user_pref.gender,
        room__room_type=str(user_pref.room_sharing),
        room__ac_type=user_pref.ac_preference,
        room__occupied_beds__lt=F('room__total_beds')
    ).exclude(user=request.user)

    for booking in bookings:
        try:
            other_pref = Preferences.objects.get(user=booking.user)
        except Preferences.DoesNotExist:
            continue

        similarity = calculate_similarity(user_pref, other_pref)

        if similarity >= 60:
            matches.append({
                'user': booking.user,
                'profile': Profile.objects.filter(user=booking.user).first(),
                'similarity': similarity,
                'room': booking.room
            })

    matches.sort(key=lambda x: x['similarity'], reverse=True)
    matches = matches[:5]

    # 🔹 If NO roommates → show empty rooms with better filtering
    empty_rooms = []
    hostel_rooms = []
    
    if not matches:
        # First, try to find empty ROOMMATE rooms
        empty_rooms = Room.objects.filter(
            room_category='ROOMMATE',
            gender=user_pref.gender,
            room_type=str(user_pref.room_sharing),
            ac_type=user_pref.ac_preference,
            occupied_beds=0
        )[:3]  # Limit to 3 suggestions
        
        # Also suggest HOSTEL_ONLY rooms as backup
        hostel_rooms = Room.objects.filter(
            room_category='HOSTEL_ONLY',
            gender=user_pref.gender,
            room_type=str(user_pref.room_sharing),
            ac_type=user_pref.ac_preference,
            occupied_beds__lt=F('total_beds')
        )[:3]  # Limit to 3 suggestions

    return render(request, 'roomieradar_app/matches.html', {
        'matches': matches,
        'empty_rooms': empty_rooms,
        'hostel_rooms': hostel_rooms,
        'user_preferences': user_pref
    })

def calculate_similarity(user_pref, candidate_pref):
    fields = [
        'bedtime',
        'cleanliness',
        'noise_tolerance',
        'guest_frequency',
        'smoking_alcohol',
        'food_type',
        'personality',
        'pet_tolerance',
        'language',
        'sharing_belongings',
        'education',
        'group_study',
        'call_frequency',
        'study_importance',
    ]

    score = 0
    total = len(fields)

    for field in fields:
        if getattr(user_pref, field, None) == getattr(candidate_pref, field, None):
            score += 1

    return round((score / total) * 100, 2)


# =================================================
# HOSTEL ONLY BOOKING
# =================================================
@login_required
def hostel_only(request):
    # ✅ CHECK: User can only book 1 bed total
    existing_booking = Booking.objects.filter(user=request.user).first()
    if existing_booking:
        messages.info(request, f"You already have a booking in Room {existing_booking.room.room_number}. You can view your booking details below.")
        return redirect('my_bookings')

    gender = request.GET.get('gender', '')
    beds = request.GET.get('beds', '')
    ac_type = request.GET.get('ac_type', '')

    rooms = Room.objects.filter(
        room_category='HOSTEL_ONLY',
        occupied_beds__lt=F('total_beds')
    )

    if gender:
        rooms = rooms.filter(gender=gender)

    if beds:
        rooms = rooms.filter(total_beds=int(beds))

    if ac_type:
        rooms = rooms.filter(ac_type=ac_type)

    # Add occupancy percentage to each room
    rooms_with_percentage = []
    for room in rooms:
        occupancy_percentage = (room.occupied_beds / room.total_beds * 100) if room.total_beds > 0 else 0
        rooms_with_percentage.append({
            'room': room,
            'occupancy_percentage': occupancy_percentage
        })

    return render(request, 'rooms/hostel_only.html', {
        'rooms_data': rooms_with_percentage,
        'rooms': rooms,  # Keep for backward compatibility
        'selected_gender': gender,
        'selected_beds': beds,
        'selected_ac_type': ac_type,
    })


# =================================================
# BOOK A BED
# =================================================
@login_required
def book_bed(request, room_id):
    room = get_object_or_404(Room, id=room_id)

    # ✅ CHECK: User can only book 1 bed total
    existing_booking = Booking.objects.filter(user=request.user).first()
    if existing_booking:
        messages.error(request, f"You already have a booking in Room {existing_booking.room.room_number}. Each user can only book one bed.")
        return redirect('my_bookings')

    # Hide full rooms
    if room.occupied_beds >= room.total_beds:
        messages.error(request, "No beds available in this room.")
        if room.room_category == 'HOSTEL_ONLY':
            return redirect('hostel_only')
        else:
            return redirect('find_matches')

    # Create booking
    Booking.objects.create(
        user=request.user,
        room=room
    )

    # Update bed count
    room.occupied_beds += 1
    room.save()

    messages.success(request, f"Successfully booked a bed in Room {room.room_number}!")
    return render(request, 'rooms/booking_success.html', {
        'room': room
    })


# =================================================
# AJAX FILTER ROOMS (HOSTEL ONLY)
# =================================================
@login_required
def ajax_filter_rooms(request):
    gender = request.GET.get('gender', '')
    beds = request.GET.get('beds', '')
    ac_type = request.GET.get('ac_type', '')

    rooms = Room.objects.filter(
        room_category='HOSTEL_ONLY',
        occupied_beds__lt=F('total_beds')
    )

    if gender:
        rooms = rooms.filter(gender=gender)

    if beds:
        rooms = rooms.filter(total_beds=int(beds))

    if ac_type:
        rooms = rooms.filter(ac_type=ac_type)

    data = []
    for room in rooms:
        data.append({
            'id': room.id,
            'room_number': room.room_number,
            'total_beds': room.total_beds,
            'occupied_beds': room.occupied_beds,
            'available_beds': room.available_beds(),
            'gender': room.gender,
            'ac_type': room.ac_type,
        })

    return JsonResponse({'rooms': data})


# =================================================
# MY BOOKINGS
# =================================================
@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user).select_related('room').order_by('-booked_at')
    
    # For each booking, get roommates (other users in the same room)
    bookings_with_roommates = []
    for booking in bookings:
        # Get all other bookings in the same room (excluding current user)
        roommate_bookings = Booking.objects.filter(
            room=booking.room
        ).exclude(user=request.user).select_related('user')
        
        # Get profiles for roommates
        roommates = []
        for rb in roommate_bookings:
            profile = Profile.objects.filter(user=rb.user).first()
            roommates.append({
                'user': rb.user,
                'profile': profile,
                'booked_at': rb.booked_at
            })
        
        bookings_with_roommates.append({
            'booking': booking,
            'roommates': roommates,
            'roommate_count': len(roommates)
        })
    
    return render(request, 'rooms/my_bookings.html', {
        'bookings': bookings,
        'bookings_with_roommates': bookings_with_roommates
    })

# =================================================
# CANCEL BOOKING (Optional)
# =================================================
@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    room = booking.room
    
    # Decrease occupied beds count
    room.occupied_beds -= 1
    room.save()
    
    # Delete booking
    booking.delete()
    
    messages.success(request, f"Your booking for Room {room.room_number} has been cancelled successfully.")
    return redirect('my_bookings')