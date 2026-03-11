from django.db import models
from django.contrib.auth.models import User


# ======================================
# ROOM MODEL
# ======================================
class Room(models.Model):

    ROOM_CATEGORY_CHOICES = [
        ('HOSTEL_ONLY', 'Hostel Only'),
        ('ROOMMATE', 'Roommate'),
    ]

    ROOM_TYPE_CHOICES = [
        ('1', 'Single'),
        ('2', '2 Sharing'),
        ('3', '3 Sharing'),
        ('4', '4 Sharing'),
    ]

    AC_CHOICES = [
        ('AC', 'AC'),
        ('NON-AC', 'Non-AC'),
    ]

    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]

    room_number = models.CharField(max_length=10)

    room_type = models.CharField(
        max_length=2,
        choices=ROOM_TYPE_CHOICES
    )

    total_beds = models.IntegerField(editable=False)
    occupied_beds = models.IntegerField(default=0)

    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    ac_type = models.CharField(max_length=10, choices=AC_CHOICES)

    room_category = models.CharField(
        max_length=20,
        choices=ROOM_CATEGORY_CHOICES,
        default='HOSTEL_ONLY'
    )

    def save(self, *args, **kwargs):
        """
        AUTO-SET total beds based on room_type
        """
        self.total_beds = int(self.room_type)
        super().save(*args, **kwargs)

    def available_beds(self):
        return self.total_beds - self.occupied_beds

    def __str__(self):
        return self.room_number

# ======================================
# BOOKING MODEL
# ======================================
class Booking(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name='bookings'
    )

    booked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} → {self.room.room_number}"
