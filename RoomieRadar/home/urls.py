from django.urls import path
from .views import landing_page, smart_matching, instant_messaging, verified_profiles

urlpatterns = [
    path('', landing_page, name='landing'),
    path('features/smart-matching/', smart_matching, name='smart_matching'),
    path('features/instant-messaging/', instant_messaging, name='instant_messaging'),
    path('features/verified-profiles/', verified_profiles, name='verified_profiles'),
]
