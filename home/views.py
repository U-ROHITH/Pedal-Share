from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from decimal import Decimal, InvalidOperation
from datetime import time

from .models import UserProfile, Cycle, Booking, Transaction


# ── Dummy data seeder ─────────────────────────────────────────────────────────

def ensure_dummy_cycles():
    if Cycle.objects.exists():
        return
    dummy = [
        {
            'owner_name': 'Jane Smith',
            'avatar_color': 'linear-gradient(135deg,#1ABC9C,#16A085)',
            'title': 'City Cruiser',
            'cycle_type': 'regular',
            'color': 'Teal',
            'price_per_hour': Decimal('20.00'),
            'location': 'Main Campus, Block A',
            'available_from': time(9, 0),
            'available_until': time(17, 0),
            'rating': Decimal('4.8'),
            'total_rides': 34,
        },
        {
            'owner_name': 'Emily White',
            'avatar_color': 'linear-gradient(135deg,#2575fc,#34495E)',
            'title': 'Blue Bolt',
            'cycle_type': 'hybrid',
            'color': 'Blue',
            'price_per_hour': Decimal('25.00'),
            'location': 'Library Gate, Block C',
            'available_from': time(13, 0),
            'available_until': time(19, 0),
            'rating': Decimal('4.6'),
            'total_rides': 22,
        },
        {
            'owner_name': 'Carlos Garcia',
            'avatar_color': 'linear-gradient(135deg,#e67e22,#d35400)',
            'title': 'Trail Blazer',
            'cycle_type': 'mountain',
            'color': 'Orange',
            'price_per_hour': Decimal('30.00'),
            'location': 'Sports Complex, Block D',
            'available_from': time(10, 0),
            'available_until': time(16, 0),
            'rating': Decimal('4.7'),
            'total_rides': 18,
        },
        {
            'owner_name': 'Priya Sharma',
            'avatar_color': 'linear-gradient(135deg,#9b59b6,#8e44ad)',
            'title': 'E-Glider',
            'cycle_type': 'electric',
            'color': 'Purple',
            'price_per_hour': Decimal('40.00'),
            'location': 'Hostel Block H, Gate 2',
            'available_from': time(8, 0),
            'available_until': time(20, 0),
            'rating': Decimal('4.9'),
            'total_rides': 51,
        },
        {
            'owner_name': 'Arjun Mehta',
            'avatar_color': 'linear-gradient(135deg,#27ae60,#2ecc71)',
            'title': 'Green Racer',
            'cycle_type': 'regular',
            'color': 'Green',
            'price_per_hour': Decimal('15.00'),
            'location': 'Cafeteria Entrance, Block B',
            'available_from': time(7, 0),
            'available_until': time(18, 0),
            'rating': Decimal('4.4'),
            'total_rides': 29,
        },
        {
            'owner_name': 'Lena Kim',
            'avatar_color': 'linear-gradient(135deg,#e74c3c,#c0392b)',
            'title': 'Red Rover',
            'cycle_type': 'hybrid',
            'color': 'Red',
            'price_per_hour': Decimal('22.00'),
            'location': 'Admin Block, Parking Lot',
            'available_from': time(11, 0),
            'available_until': time(21, 0),
            'rating': Decimal('4.5'),
            'total_rides': 15,
        },
    ]
    for d in dummy:
        Cycle.objects.create(**d)


# ── Public views ──────────────────────────────────────────────────────────────

def frontend(request):
    ensure_dummy_cycles()
    featured = Cycle.objects.filter(is_available=True).order_by('-rating')[:3]
    return render(request, 'frontend.html', {'featured_cycles': featured})


def base(request):
    return render(request, 'base.html')


def aboutus(request):
    return render(request, 'aboutus.html')


def contactus(request):
    if request.method == 'POST':
        messages.success(request, "Thanks for reaching out! We'll get back to you within 24 hours.")
        return redirect('contactus')
    return render(request, 'contactus.html')


def raiseacomplaint(request):
    if request.method == 'POST':
        messages.success(request, 'Your complaint has been submitted. We will review it and respond within 48 hours.')
        return redirect('raiseacomplaint')
    return render(request, 'raiseacomplaint.html')


def help_page(request):
    return render(request, 'help.html')


def login_page(request):
    return redirect('signin')


def availablecycles(request):
    ensure_dummy_cycles()
    all_cycles = Cycle.objects.all().order_by('-is_available', '-rating')
    return render(request, 'availablecycles.html', {'cycles': all_cycles})


# ── Auth views ────────────────────────────────────────────────────────────────

def signin(request):
    if request.user.is_authenticated:
        return redirect('home')
    next_url = request.GET.get('next', '') or request.POST.get('next', '')
    if request.method == 'POST':
        email    = request.POST.get('email', '').strip().lower()
        password = request.POST.get('password', '')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect(next_url) if next_url else redirect('home')
        messages.error(request, 'Invalid email or password.')
    return render(request, 'signin.html', {'next': next_url})


def signup(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        full_name = request.POST.get('full_name', '').strip()
        email     = request.POST.get('email', '').strip().lower()
        phone     = request.POST.get('phone', '').strip()
        password  = request.POST.get('password', '')
        confirm   = request.POST.get('confirm_password', '')

        if not full_name:
            messages.error(request, 'Full name is required.')
        elif not email:
            messages.error(request, 'Email is required.')
        elif password != confirm:
            messages.error(request, 'Passwords do not match.')
        elif len(password) < 8:
            messages.error(request, 'Password must be at least 8 characters.')
        elif User.objects.filter(username=email).exists():
            messages.error(request, 'An account with this email already exists.')
        else:
            parts = full_name.split(' ', 1)
            user = User.objects.create_user(
                username=email,
                email=email,
                password=password,
                first_name=parts[0],
                last_name=parts[1] if len(parts) > 1 else '',
            )
            # Signal already created profile; update extra fields
            profile = user.profile
            profile.full_name = full_name
            profile.phone = phone
            profile.save()
            # Welcome bonus ledger entry (balance already ₹500 from model default)
            Transaction.objects.create(
                user=user,
                amount=Decimal('500.00'),
                transaction_type='credit',
                description='Welcome bonus — ₹500 added on signup',
            )
            login(request, user)
            messages.success(request, f'Welcome, {parts[0]}! ₹500 has been added to your wallet.')
            return redirect('home')
    return render(request, 'signup.html')


def signout(request):
    logout(request)
    return redirect('home')


# ── Booking views ─────────────────────────────────────────────────────────────

@login_required
def book_cycle(request, cycle_id):
    if request.method != 'POST':
        return redirect('availablecycles')

    cycle = get_object_or_404(Cycle, pk=cycle_id)

    if not cycle.is_available:
        messages.error(request, 'This cycle is no longer available.')
        return redirect('availablecycles')

    if cycle.owner == request.user:
        messages.error(request, "You can't book your own cycle.")
        return redirect('availablecycles')

    try:
        hours = max(1, int(request.POST.get('hours', 1)))
    except ValueError:
        hours = 1

    total = cycle.price_per_hour * hours
    profile = request.user.profile

    if profile.wallet_balance < total:
        messages.error(
            request,
            f'Insufficient balance. Need ₹{total}, you have ₹{profile.wallet_balance}. '
            f'Please add money to your wallet.'
        )
        return redirect('wallet')

    # Atomic: deduct wallet, create booking & transaction, mark cycle unavailable
    profile.wallet_balance -= total
    profile.save()

    cycle.is_available = False
    cycle.total_rides += 1
    cycle.save()

    Booking.objects.create(
        user=request.user,
        cycle=cycle,
        hours=hours,
        total_amount=total,
        status='active',
    )
    Transaction.objects.create(
        user=request.user,
        amount=total,
        transaction_type='debit',
        description=f'Booked "{cycle.title}" for {hours} hr(s)',
    )

    messages.success(request, f'Booking confirmed! ₹{total} deducted. Enjoy your ride!')
    return redirect('my_bookings')


@login_required
def cancel_booking(request, booking_id):
    if request.method != 'POST':
        return redirect('my_bookings')

    booking = get_object_or_404(Booking, pk=booking_id, user=request.user, status='active')
    profile = request.user.profile

    # Full refund
    profile.wallet_balance += booking.total_amount
    profile.save()

    booking.status = 'cancelled'
    booking.save()

    booking.cycle.is_available = True
    booking.cycle.save()

    Transaction.objects.create(
        user=request.user,
        amount=booking.total_amount,
        transaction_type='credit',
        description=f'Refund — cancelled booking for "{booking.cycle.title}"',
    )

    messages.success(request, f'Booking cancelled. ₹{booking.total_amount} refunded to your wallet.')
    return redirect('my_bookings')


@login_required
def complete_booking(request, booking_id):
    if request.method != 'POST':
        return redirect('my_bookings')

    booking = get_object_or_404(Booking, pk=booking_id, user=request.user, status='active')
    booking.status = 'completed'
    booking.save()

    booking.cycle.is_available = True
    booking.cycle.save()

    messages.success(request, f'Ride completed! Hope you enjoyed "{booking.cycle.title}".')
    return redirect('my_bookings')


@login_required
def my_bookings(request):
    bookings = request.user.bookings.select_related('cycle').order_by('-booked_at')
    return render(request, 'my_bookings.html', {'bookings': bookings})


# ── Wallet view ───────────────────────────────────────────────────────────────

@login_required
def wallet(request):
    profile      = request.user.profile
    transactions = request.user.transactions.order_by('-created_at')[:20]

    if request.method == 'POST':
        try:
            amount = Decimal(request.POST.get('amount', '0'))
            if amount <= 0:
                raise ValueError
        except (InvalidOperation, ValueError):
            messages.error(request, 'Please enter a valid amount.')
            return redirect('wallet')

        if amount > Decimal('10000'):
            messages.error(request, 'Maximum top-up per transaction is ₹10,000.')
            return redirect('wallet')

        profile.wallet_balance += amount
        profile.save()
        Transaction.objects.create(
            user=request.user,
            amount=amount,
            transaction_type='credit',
            description='Wallet top-up via payment gateway',
        )
        messages.success(request, f'₹{amount} added to your wallet!')
        return redirect('wallet')

    return render(request, 'wallet.html', {
        'profile': profile,
        'transactions': transactions,
    })


@login_required
def PaymentGateway(request):
    if request.method == 'POST':
        try:
            amount = Decimal(request.POST.get('amount', '0'))
            if amount <= 0:
                raise ValueError
        except (InvalidOperation, ValueError):
            messages.error(request, 'Please enter a valid amount.')
            return redirect('payment_gateway')
        if amount > Decimal('10000'):
            messages.error(request, 'Maximum top-up per transaction is ₹10,000.')
            return redirect('payment_gateway')
        profile = request.user.profile
        profile.wallet_balance += amount
        profile.save()
        Transaction.objects.create(
            user=request.user,
            amount=amount,
            transaction_type='credit',
            description='Wallet top-up via payment gateway',
        )
        messages.success(request, f'₹{amount} added to your wallet successfully!')
        return redirect('wallet')
    return render(request, 'PaymentGateway.html')


# ── Cycle listing (user-owned) ─────────────────────────────────────────────────

# Map a human colour name → a CSS gradient for the avatar strip
_COLOR_GRADIENTS = {
    'black':  'linear-gradient(135deg,#2c3e50,#4a4a4a)',
    'white':  'linear-gradient(135deg,#bdc3c7,#95a5a6)',
    'red':    'linear-gradient(135deg,#e74c3c,#c0392b)',
    'blue':   'linear-gradient(135deg,#2575fc,#34495E)',
    'green':  'linear-gradient(135deg,#27ae60,#2ecc71)',
    'yellow': 'linear-gradient(135deg,#f39c12,#e67e22)',
    'orange': 'linear-gradient(135deg,#e67e22,#d35400)',
    'purple': 'linear-gradient(135deg,#9b59b6,#8e44ad)',
    'pink':   'linear-gradient(135deg,#fd79a8,#e84393)',
    'teal':   'linear-gradient(135deg,#1ABC9C,#16A085)',
    'grey':   'linear-gradient(135deg,#7f8c8d,#636e72)',
    'gray':   'linear-gradient(135deg,#7f8c8d,#636e72)',
}


@login_required
def my_cycles(request):
    cycles = request.user.cycles.order_by('-id')
    return render(request, 'my_cycles.html', {'cycles': cycles})


@login_required
def add_cycle(request):
    if request.method == 'POST':
        title          = request.POST.get('title', '').strip()
        cycle_type     = request.POST.get('cycle_type', 'regular')
        color          = request.POST.get('color', '').strip()
        price_str      = request.POST.get('price_per_hour', '').strip()
        location       = request.POST.get('location', '').strip()
        available_from = request.POST.get('available_from', '').strip()
        available_until = request.POST.get('available_until', '').strip()

        # Validate
        errors = []
        if not title:
            errors.append('Cycle title is required.')
        if not color:
            errors.append('Colour is required.')
        if not location:
            errors.append('Location is required.')
        if not available_from or not available_until:
            errors.append('Availability times are required.')

        price = None
        try:
            price = Decimal(price_str)
            if price <= 0:
                raise ValueError
        except (InvalidOperation, ValueError):
            errors.append('Enter a valid price per hour (e.g. 20).')

        if errors:
            for e in errors:
                messages.error(request, e)
            color_options = [
                {'name': 'Teal',   'gradient': 'linear-gradient(135deg,#1ABC9C,#16A085)'},
                {'name': 'Blue',   'gradient': 'linear-gradient(135deg,#2575fc,#34495E)'},
                {'name': 'Green',  'gradient': 'linear-gradient(135deg,#27ae60,#2ecc71)'},
                {'name': 'Red',    'gradient': 'linear-gradient(135deg,#e74c3c,#c0392b)'},
                {'name': 'Orange', 'gradient': 'linear-gradient(135deg,#e67e22,#d35400)'},
                {'name': 'Purple', 'gradient': 'linear-gradient(135deg,#9b59b6,#8e44ad)'},
                {'name': 'Pink',   'gradient': 'linear-gradient(135deg,#fd79a8,#e84393)'},
                {'name': 'Yellow', 'gradient': 'linear-gradient(135deg,#f39c12,#e67e22)'},
                {'name': 'Black',  'gradient': 'linear-gradient(135deg,#2c3e50,#4a4a4a)'},
                {'name': 'Grey',   'gradient': 'linear-gradient(135deg,#7f8c8d,#636e72)'},
            ]
            return render(request, 'add_cycle.html', {'post': request.POST, 'color_options': color_options})

        # Build avatar gradient from colour
        gradient = _COLOR_GRADIENTS.get(color.lower(), 'linear-gradient(135deg,#1ABC9C,#16A085)')
        profile = request.user.profile
        full_name = profile.full_name or request.user.get_full_name() or request.user.username

        Cycle.objects.create(
            owner=request.user,
            owner_name=full_name,
            avatar_color=gradient,
            title=title,
            cycle_type=cycle_type,
            color=color.capitalize(),
            price_per_hour=price,
            location=location,
            available_from=available_from,
            available_until=available_until,
        )
        messages.success(request, f'"{title}" has been listed successfully!')
        return redirect('my_cycles')

    color_options = [
        {'name': 'Teal',   'gradient': 'linear-gradient(135deg,#1ABC9C,#16A085)'},
        {'name': 'Blue',   'gradient': 'linear-gradient(135deg,#2575fc,#34495E)'},
        {'name': 'Green',  'gradient': 'linear-gradient(135deg,#27ae60,#2ecc71)'},
        {'name': 'Red',    'gradient': 'linear-gradient(135deg,#e74c3c,#c0392b)'},
        {'name': 'Orange', 'gradient': 'linear-gradient(135deg,#e67e22,#d35400)'},
        {'name': 'Purple', 'gradient': 'linear-gradient(135deg,#9b59b6,#8e44ad)'},
        {'name': 'Pink',   'gradient': 'linear-gradient(135deg,#fd79a8,#e84393)'},
        {'name': 'Yellow', 'gradient': 'linear-gradient(135deg,#f39c12,#e67e22)'},
        {'name': 'Black',  'gradient': 'linear-gradient(135deg,#2c3e50,#4a4a4a)'},
        {'name': 'Grey',   'gradient': 'linear-gradient(135deg,#7f8c8d,#636e72)'},
    ]
    return render(request, 'add_cycle.html', {'post': {}, 'color_options': color_options})


@login_required
def delete_cycle(request, cycle_id):
    if request.method != 'POST':
        return redirect('my_cycles')
    cycle = get_object_or_404(Cycle, pk=cycle_id, owner=request.user)

    # Refund any active booking before deleting
    active_booking = cycle.bookings.filter(status='active').first()
    if active_booking:
        booker_profile = active_booking.user.profile
        booker_profile.wallet_balance += active_booking.total_amount
        booker_profile.save()
        Transaction.objects.create(
            user=active_booking.user,
            amount=active_booking.total_amount,
            transaction_type='credit',
            description=f'Refund — "{cycle.title}" was removed by the owner',
        )
        active_booking.status = 'cancelled'
        active_booking.save()

    name = cycle.title
    cycle.delete()
    messages.success(request, f'"{name}" has been removed from listings.')
    return redirect('my_cycles')


@login_required
def toggle_cycle(request, cycle_id):
    if request.method != 'POST':
        return redirect('my_cycles')
    cycle = get_object_or_404(Cycle, pk=cycle_id, owner=request.user)
    # Block toggling to "available" while there is an active booking
    if not cycle.is_available and cycle.bookings.filter(status='active').exists():
        messages.error(request, f'"{cycle.title}" has an active booking — it will become available once the ride is completed or cancelled.')
        return redirect('my_cycles')
    cycle.is_available = not cycle.is_available
    cycle.save()
    state = 'available' if cycle.is_available else 'unavailable'
    messages.success(request, f'"{cycle.title}" marked as {state}.')
    return redirect('my_cycles')
