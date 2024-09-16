from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('rooms/', views.rooms, name='rooms'),
    path('booking/<int:room_id>/', views.booking, name='booking'),
     path('payment/<int:booking_id>/',views.payment, name='payment'),
    path('booking_confirmation/', views.booking_confirmation, name='booking_confirmation'),  # Added comma here
    path('confirmation/', views.confirmation, name='confirmation'),
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
