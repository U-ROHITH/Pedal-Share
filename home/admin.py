from django.contrib import admin
from .models import UserProfile, Cycle, Booking, Transaction

admin.site.register(UserProfile)
admin.site.register(Cycle)
admin.site.register(Booking)
admin.site.register(Transaction)
