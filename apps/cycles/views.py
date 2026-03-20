from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.db.models import Q
from apps.cycles.models import Cycle
from apps.cycles.forms import CycleForm, CycleFilterForm


def available_cycles(request):
    """List all available cycles with filtering"""
    cycles = Cycle.objects.filter(is_active=True, is_available=True)
    form = CycleFilterForm(request.GET or None)
    
    if form.is_valid():
        if form.cleaned_data.get('cycle_type'):
            cycles = cycles.filter(cycle_type=form.cleaned_data['cycle_type'])
        if form.cleaned_data.get('min_price'):
            cycles = cycles.filter(price_per_hour__gte=form.cleaned_data['min_price'])
        if form.cleaned_data.get('max_price'):
            cycles = cycles.filter(price_per_hour__lte=form.cleaned_data['max_price'])
        if form.cleaned_data.get('location'):
            cycles = cycles.filter(location__icontains=form.cleaned_data['location'])
    
    return render(request, 'cycles/list.html', {'cycles': cycles, 'form': form})


def cycle_detail(request, cycle_id):
    """Show cycle details"""
    cycle = get_object_or_404(Cycle, id=cycle_id, is_active=True)
    bookings_count = cycle.bookings.filter(status='completed').count()
    
    context = {
        'cycle': cycle,
        'bookings_count': bookings_count,
    }
    return render(request, 'cycles/detail.html', context)


@login_required(login_url='users:signin')
@require_http_methods(["GET", "POST"])
def add_cycle(request):
    """Add a new cycle"""
    if request.method == 'POST':
        form = CycleForm(request.POST, request.FILES)
        if form.is_valid():
            cycle = form.save(commit=False)
            cycle.owner = request.user
            cycle.save()
            messages.success(request, 'Cycle added successfully!')
            return redirect('cycles:my_cycles')
    else:
        form = CycleForm()
    
    return render(request, 'cycles/add.html', {'form': form})


@login_required(login_url='users:signin')
@require_http_methods(["GET", "POST"])
def edit_cycle(request, cycle_id):
    """Edit cycle details"""
    cycle = get_object_or_404(Cycle, id=cycle_id, owner=request.user)
    
    if request.method == 'POST':
        form = CycleForm(request.POST, request.FILES, instance=cycle)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cycle updated successfully!')
            return redirect('cycles:my_cycles')
    else:
        form = CycleForm(instance=cycle)
    
    return render(request, 'cycles/edit.html', {'form': form, 'cycle': cycle})


@login_required(login_url='users:signin')
@require_http_methods(["POST"])
def delete_cycle(request, cycle_id):
    """Delete a cycle"""
    cycle = get_object_or_404(Cycle, id=cycle_id, owner=request.user)
    cycle.delete()
    messages.success(request, 'Cycle deleted successfully!')
    return redirect('cycles:my_cycles')


@login_required(login_url='users:signin')
@require_http_methods(["GET"])
def my_cycles(request):
    """List user's own cycles"""
    cycles = Cycle.objects.filter(owner=request.user)
    
    context = {
        'cycles': cycles,
        'total_cycles': cycles.count(),
        'active_cycles': cycles.filter(is_available=True).count(),
    }
    return render(request, 'cycles/my_cycles.html', context)


@login_required(login_url='users:signin')
@require_http_methods(["POST"])
def toggle_cycle_availability(request, cycle_id):
    """Toggle cycle availability"""
    cycle = get_object_or_404(Cycle, id=cycle_id, owner=request.user)
    cycle.is_available = not cycle.is_available
    cycle.save()
    
    status = "available" if cycle.is_available else "unavailable"
    messages.success(request, f'Cycle marked as {status}.')
    return redirect('cycles:my_cycles')
