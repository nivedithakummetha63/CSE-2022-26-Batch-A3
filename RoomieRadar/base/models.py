from django.db import models
from django.contrib.auth.models import User
import uuid


# ======================================
# PROFILE MODEL (USER DETAILS)
# ======================================
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Basic profile info
    age = models.IntegerField(null=True, blank=True)
    gender = models.CharField(
        max_length=10,
        choices=[
            ('Male', 'Male'),
            ('Female', 'Female'),
            ('Other', 'Other'),
        ],
        null=True,
        blank=True
    )
    bio = models.TextField(blank=True)
    photo = models.ImageField(upload_to='profiles/', blank=True, null=True)

    # Email verification
    email_token = models.UUIDField(default=uuid.uuid4, unique=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


# ======================================
# PREFERENCES MODEL (ROOMMATE MATCHING)
# ======================================

class Preferences(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Mandatory (but filled later)
    gender = models.CharField(max_length=10, null=True, blank=True)
    room_sharing = models.IntegerField(null=True, blank=True)
    ac_preference = models.CharField(max_length=10, null=True, blank=True)

    # Lifestyle
    bedtime = models.CharField(max_length=20, null=True, blank=True)
    cleanliness = models.CharField(max_length=20, null=True, blank=True)
    noise_tolerance = models.CharField(max_length=20, null=True, blank=True)
    guest_frequency = models.CharField(max_length=20, null=True, blank=True)

    smoking = models.CharField(max_length=20, null=True, blank=True)
    food_type = models.CharField(max_length=20, null=True, blank=True)
    personality = models.CharField(max_length=20, null=True, blank=True)
    pet_tolerance = models.CharField(max_length=10, null=True, blank=True)
    language = models.CharField(max_length=20, null=True, blank=True)
    sharing_belongings = models.CharField(max_length=10, null=True, blank=True)
    education = models.CharField(max_length=50, null=True, blank=True)
    group_study = models.CharField(max_length=10, null=True, blank=True)
    call_frequency = models.CharField(max_length=10, null=True, blank=True)
    study_importance = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} Preferences"
