from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Room, Booking, Payment
from django.http import HttpResponse
from django.contrib import messages
from .models import UserSignUp
from django.contrib.auth.decorators import login_required
from django.utils import timezone


def home(request):
    return render(request, 'home.html')


def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        if UserSignUp.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken. Please choose another one.')
            return redirect('signup')

        if UserSignUp.objects.filter(email=email).exists():
            messages.error(request, 'Email already taken. Please choose another one.')
            return redirect('signup')

        user_signup = UserSignUp(username=username, email=email, password=password)
        user_signup.save()

        # Create the user in the User model
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        # Authenticate and log in the user
        user = authenticate(username=username, password=password)
        if user is not None:
            auth_login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('login')  # Redirect to home page after signup and login

    return render(request, 'signup.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('rooms')  # Redirect to rooms page after login
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('login')
    return render(request, 'login.html')


def rooms(request):
    # Retrieve all rooms from the database
    rooms = Room.objects.all()
    
    # Organize rooms by room type
    room_types = Room.ROOM_TYPE_CHOICES
    categorized_rooms = {room_type[0]: rooms.filter(room_type=room_type[0]) for room_type in room_types}
    
    context = {
        'categorized_rooms': categorized_rooms
    }
    
    return render(request, 'rooms.html', context)


@login_required
def booking(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    
    if request.method == 'POST':
        # Extract form data
        name = request.POST.get('name')
        email = request.POST.get('email')
        checkin = request.POST.get('checkin')
        checkout = request.POST.get('checkout')
        
        # Ensure that you correctly handle the room_id (it's redundant to fetch it again)
        # If the room_id is passed in the URL, it is already available as room_id
        
        # Create a new booking
        booking = Booking.objects.create(
            user=request.user,
            room=room,
            checkin_date=checkin,
            checkout_date=checkout,
            is_confirmed=False,
            booking_date=timezone.now()
        )
        
        # Redirect to the payment page with the booking_id
        return redirect('payment', booking_id=booking.id)
    
    return render(request, 'booking.html', {'room': room})


def booking_confirmation(request):
    booking_id = request.GET.get('booking_id')
    if not booking_id:
        return redirect('rooms')  # Redirect to rooms if no booking ID is provided

    booking = get_object_or_404(Booking, id=booking_id)
    return render(request, 'booking_confirmation.html', {
        'booking': booking,
        'room': booking.room,
        'checkin': booking.checkin_date,
        'checkout': booking.checkout_date
    })


def payment(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    if request.method == 'POST':
        # Get form data
        card_number = request.POST.get('card_number')
        card_name = request.POST.get('card_name')
        expiry_date = request.POST.get('expiry_date')
        cvv = request.POST.get('cvv')

        # Check that all required fields are provided
        if not all([card_number, card_name, expiry_date, cvv]):
            return render(request, 'payment.html', {
                'booking': booking,
                'error': 'All fields are required.'
            })

        # Create payment record
        Payment.objects.create(
            booking=booking,
            amount=booking.room.price,
            cardholder_name=card_name,
            card_number=card_number,
            expiry_date=expiry_date,
            cvv=cvv,
            payment_status='Paid'
        )

        # Mark room as booked
        booking.room.is_booked = True
        booking.room.save()

        return redirect('booking_confirmation')  # Redirect to confirmation page after payment

    context = {
        'booking': booking,
        'room_description': booking.room.description,
        'room_price': booking.room.price,
        'booking_id': booking.id
    }
    return render(request, 'payment.html', context)

def confirmation(request):
    return render(request, 'confirmation.html', {'message': 'Your booking and payment were successful!'})