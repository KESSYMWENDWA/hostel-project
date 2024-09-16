from django.contrib import admin
from .models import Room, Booking, Payment

class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'room', 'checkin_date', 'checkout_date', 'is_confirmed', 'booking_date')
    list_filter = ('is_confirmed', 'booking_date')
    search_fields = ('user_username', 'room_room_number')

admin.site.register(Room)
admin.site.register(Booking, BookingAdmin)
admin.site.register(Payment)