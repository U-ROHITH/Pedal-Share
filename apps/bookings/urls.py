from django.urls import path
from apps.bookings import views

app_name = 'bookings'

urlpatterns = [
    path('book/<int:cycle_id>/', views.book_cycle, name='book'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('detail/<int:booking_id>/', views.booking_detail, name='detail'),
    path('cancel/<int:booking_id>/', views.cancel_booking, name='cancel'),
    path('complete/<int:booking_id>/', views.complete_booking, name='complete'),
]
