from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class UserSignUp(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)

    def str(self):
        return self.username

class Room(models.Model):
    ROOM_TYPE_CHOICES = [
        ('single', 'Single'),
        ('double', 'Double'),
        ('suite', 'Suite'),
    ]
    
    room_number = models.CharField(max_length=10)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_booked = models.BooleanField(default=False)
    room_type = models.CharField(max_length=10, choices=ROOM_TYPE_CHOICES)
    image = models.ImageField(upload_to='room_images/')

    def _str_(self):
        return f'{self.room_number} - {self.room_type}'

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    checkin_date = models.DateField()
    checkout_date = models.DateField()
    is_confirmed = models.BooleanField(default=False)
    booking_date = models.DateTimeField(default=timezone.now)

    def _str_(self):
        return f"Booking for Room {self.room.room_number} by {self.user.username}"

class Payment(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    cardholder_name = models.CharField(max_length=100, default='Unknown')
    card_number = models.CharField(max_length=16, blank=True)  # No default, allow empty for existing rows
    expiry_date = models.CharField(max_length=5, blank=True)   # Allow empty
    cvv = models.CharField(max_length=4, blank=True)           # Allow empty
    payment_status = models.CharField(max_length=10, default='Pending')

    def _str_(self):
        return f"Payment for booking {self.booking.id}"