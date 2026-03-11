
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from base.models import Profile, Preferences
from roomieradar_app.models import Booking
from .match_utils import find_best_matches
from datetime import date
@login_required
def app_home(request):
    return render(request, 'base/app_home.html')
@login_required
def with_roommate(request):
    existing_booking = Booking.objects.filter(user=request.user).first()
    
    return render(request, 'base/with_roommate.html', {
        'existing_booking': existing_booking
    })
@login_required
def profile_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == "POST":
        profile.age = request.POST.get('age') or profile.age
        profile.gender = request.POST.get('gender') or profile.gender
        profile.bio = request.POST.get('bio') or profile.bio

        # Handle image upload
        if request.FILES.get('photo'):
            profile.photo = request.FILES.get('photo')

        profile.save()
        return redirect('profile')  # redirect back to profile page

    # Calculate stats
    booking_count = Booking.objects.filter(user=request.user).count()
    has_preferences = Preferences.objects.filter(user=request.user).exists()
    prefs = Preferences.objects.filter(user=request.user).first()
    if prefs and prefs.gender and prefs.room_sharing and prefs.ac_preference:
        has_preferences = True
    
    # Calculate days since joining
    days_active = (date.today() - request.user.date_joined.date()).days
    
    return render(request, 'base/profile.html', {
        'profile': profile,
        'booking_count': booking_count,
        'has_preferences': has_preferences,
        'days_active': days_active
    })
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from base.models import Preferences

@login_required
def preferences_view(request):
    prefs, created = Preferences.objects.get_or_create(user=request.user)

    if request.method == "POST":
        prefs.gender = request.POST.get('gender')
        prefs.room_sharing = request.POST.get('room_sharing')
        prefs.ac_preference = request.POST.get('ac_preference')

        prefs.bedtime = request.POST.get('bedtime')
        prefs.cleanliness = request.POST.get('cleanliness')
        prefs.noise_tolerance = request.POST.get('noise_tolerance')
        prefs.guest_frequency = request.POST.get('guest_frequency')
        prefs.smoking = request.POST.get('smoking')
        prefs.food_type = request.POST.get('food_type')
        prefs.personality = request.POST.get('personality')
        prefs.pet_tolerance = request.POST.get('pet_tolerance')
        prefs.language = request.POST.get('language')
        prefs.sharing_belongings = request.POST.get('sharing_belongings')
        prefs.education = request.POST.get('education')
        prefs.group_study = request.POST.get('group_study')
        prefs.call_frequency = request.POST.get('call_frequency')
        prefs.study_importance = request.POST.get('study_importance')

        prefs.save()

        return redirect('preferences')  # reload with saved data

    return render(request, 'base/preferences.html', {
        'prefs': prefs
    })


from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

@login_required
def view_user_profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    profile, _ = Profile.objects.get_or_create(user=user)

    return render(request, 'base/view_profile.html', {
        'profile': profile,
        'viewed_user': user
    })

