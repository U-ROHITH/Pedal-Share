from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from apps.bookings.models import Booking
from apps.bookings.forms import BookingForm
from apps.cycles.models import Cycle


@login_required(login_url='users:signin')
@require_http_methods(["GET", "POST"])
def book_cycle(request, cycle_id):
    """Create a booking for a cycle"""
    cycle = get_object_or_404(Cycle, id=cycle_id, is_active=True, is_available=True)
    
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.cycle = cycle
            booking.calculate_total_price()
            booking.save()
            messages.success(request, 'Booking created! Proceed to payment.')
            return redirect('payments:checkout', booking_id=booking.id)
    else:
        form = BookingForm()
    
    context = {
        'cycle': cycle,
        'form': form,
    }
    return render(request, 'bookings/confirm.html', context)


@login_required(login_url='users:signin')
@require_http_methods(["GET"])
def my_bookings(request):
    """View user's bookings"""
    bookings = Booking.objects.filter(user=request.user).select_related('cycle')
    
    active = bookings.filter(status='active')
    completed = bookings.filter(status='completed')
    cancelled = bookings.filter(status='cancelled')
    
    context = {
        'bookings': bookings,
        'active_count': active.count(),
        'completed_count': completed.count(),
        'cancelled_count': cancelled.count(),
    }
    return render(request, 'bookings/list.html', context)


@login_required(login_url='users:signin')
@require_http_methods(["GET"])
def booking_detail(request, booking_id):
    """View booking details"""
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    return render(request, 'bookings/detail.html', {'booking': booking})


@login_required(login_url='users:signin')
@require_http_methods(["POST"])
def cancel_booking(request, booking_id):
    """Cancel a booking"""
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    
    if booking.status in ['pending', 'active']:
        booking.status = 'cancelled'
        booking.save()
        messages.success(request, 'Booking cancelled successfully.')
    else:
        messages.error(request, 'Cannot cancel this booking.')
    
    return redirect('bookings:my_bookings')


@login_required(login_url='users:signin')
@require_http_methods(["POST"])
def complete_booking(request, booking_id):
    """Mark booking as completed"""
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    
    if booking.status == 'active':
        booking.status = 'completed'
        booking.save()
        messages.success(request, 'Booking completed.')
    
    return redirect('bookings:my_bookings')
