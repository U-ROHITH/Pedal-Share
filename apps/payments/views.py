from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.db.models import Sum
from decimal import Decimal
from apps.payments.models import Transaction
from apps.payments.forms import WalletTopupForm
from apps.bookings.models import Booking


@login_required(login_url='users:signin')
@require_http_methods(["GET"])
def wallet(request):
    """View wallet balance and transaction history"""
    profile = request.user.profile
    transactions = Transaction.objects.filter(user=request.user)
    
    # Calculate stats
    topups = transactions.filter(transaction_type='wallet_topup', status='success')
    refunds = transactions.filter(transaction_type='refund', status='success')
    
    total_topups_amount = topups.aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
    total_refunds_amount = refunds.aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
    
    context = {
        'profile': profile,
        'transactions': transactions[:10],  # Latest 10 transactions
        'total_topups': total_topups_amount,
        'total_refunds': total_refunds_amount,
    }
    return render(request, 'payments/wallet.html', context)


@login_required(login_url='users:signin')
@require_http_methods(["GET", "POST"])
def topup_wallet(request):
    """Handle wallet top-up"""
    if request.method == 'POST':
        form = WalletTopupForm(request.POST)
        if form.is_valid():
            amount_preset = form.cleaned_data['amount_preset']
            
            if amount_preset == 'custom':
                amount = form.cleaned_data.get('custom_amount')
                if not amount or amount < Decimal('10'):
                    messages.error(request, 'Custom amount must be at least ₹10.')
                    return redirect('payments:topup_wallet')
            else:
                amount = Decimal(amount_preset)
            
            # In a real app, integrate with payment gateway (Razorpay, Stripe, etc.)
            # For now, we'll create a pending transaction
            transaction = Transaction.objects.create(
                user=request.user,
                transaction_type='wallet_topup',
                amount=amount,
                description=f'Flat Topup - ₹{amount}',
                status='pending'
            )
            
            # Redirect to payment gateway
            return redirect('payments:payment_gateway', transaction_id=transaction.id)
    else:
        form = WalletTopupForm()
    
    return render(request, 'payments/topup.html', {'form': form})


@login_required(login_url='users:signin')
@require_http_methods(["GET"])
def payment_gateway(request, transaction_id):
    """Payment gateway simulation"""
    transaction = get_object_or_404(Transaction, id=transaction_id, user=request.user)
    
    context = {
        'transaction': transaction,
        'amount': transaction.amount,
    }
    return render(request, 'payments/payment_gateway.html', context)


@login_required(login_url='users:signin')
@require_http_methods(["POST"])
def process_payment(request, transaction_id):
    """Process payment (simplified - integrate with actual payment gateway)"""
    transaction = get_object_or_404(Transaction, id=transaction_id, user=request.user)
    profile = request.user.profile
    
    # Simulate payment processing
    balance_before = profile.wallet_balance
    profile.wallet_balance += transaction.amount
    profile.save()
    
    transaction.balance_before = balance_before
    transaction.balance_after = profile.wallet_balance
    transaction.status = 'success'
    transaction.save()
    
    messages.success(request, f'₹{transaction.amount} added to your wallet!')
    return redirect('payments:wallet')


@login_required(login_url='users:signin')
@require_http_methods(["GET"])
def booking_checkout(request, booking_id):
    """Checkout page for booking payment"""
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    profile = request.user.profile
    
    context = {
        'booking': booking,
        'profile': profile,
        'can_pay_from_wallet': profile.wallet_balance >= booking.total_price,
    }
    return render(request, 'payments/checkout.html', context)


@login_required(login_url='users:signin')
@require_http_methods(["POST"])
def pay_with_wallet(request, booking_id):
    """Pay for booking using wallet"""
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    profile = request.user.profile
    
    if profile.wallet_balance >= booking.total_price:
        profile.wallet_balance -= booking.total_price
        profile.save()
        
        booking.status = 'active'
        booking.payment_status = 'paid'
        booking.save()
        
        Transaction.objects.create(
            user=request.user,
            transaction_type='booking_payment',
            amount=booking.total_price,
            description=f'Booking {booking.id} - {booking.cycle.title}',
            booking=booking,
            balance_before=profile.wallet_balance + booking.total_price,
            balance_after=profile.wallet_balance,
            status='success'
        )
        
        messages.success(request, 'Booking confirmed!')
        return redirect('bookings:my_bookings')
    else:
        messages.error(request, 'Insufficient wallet balance.')
        return redirect('payments:booking_checkout', booking_id=booking_id)
