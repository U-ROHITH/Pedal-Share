from django.urls import path
from home import views

urlpatterns = [
    # Home
    path("", views.frontend, name='home'),
    path("frontend.html", views.frontend, name='frontend'),
    path("base.html", views.base, name='base'),

    # Info pages
    path("aboutus.html", views.aboutus, name='aboutus'),
    path("contactus.html", views.contactus, name='contactus'),
    path("raiseacomplaint.html", views.raiseacomplaint, name='raiseacomplaint'),
    path("help/", views.help_page, name='help'),

    # Auth
    path("signin.html", views.signin, name='signin'),
    path("signup.html", views.signup, name='signup'),
    path("signout/", views.signout, name='signout'),
    path("Login.html", views.login_page, name='login'),

    # Cycles & bookings
    path("availablecycles.html", views.availablecycles, name='availablecycles'),
    path("book/<int:cycle_id>/", views.book_cycle, name='book_cycle'),
    path("cancel/<int:booking_id>/", views.cancel_booking, name='cancel_booking'),
    path("complete/<int:booking_id>/", views.complete_booking, name='complete_booking'),
    path("my-bookings/", views.my_bookings, name='my_bookings'),

    # Wallet
    path("wallet.html", views.wallet, name='wallet'),
    path("PaymentGateway.html", views.PaymentGateway, name='payment_gateway'),

    # User cycle listings
    path("my-cycles/", views.my_cycles, name='my_cycles'),
    path("add-cycle/", views.add_cycle, name='add_cycle'),
    path("delete-cycle/<int:cycle_id>/", views.delete_cycle, name='delete_cycle'),
    path("toggle-cycle/<int:cycle_id>/", views.toggle_cycle, name='toggle_cycle'),
]
