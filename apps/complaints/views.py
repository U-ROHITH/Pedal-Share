from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from apps.complaints.models import Complaint
from apps.complaints.forms import ComplaintForm


@login_required(login_url='users:signin')
@require_http_methods(["GET", "POST"])
def raise_complaint(request):
    """Raise a new complaint"""
    if request.method == 'POST':
        form = ComplaintForm(request.POST)
        if form.is_valid():
            complaint = form.save(commit=False)
            complaint.user = request.user
            complaint.save()
            messages.success(request, 'Your complaint has been filed. We will get back to you soon.')
            return redirect('complaints:my_complaints')
    else:
        form = ComplaintForm()
    
    return render(request, 'complaints/raise.html', {'form': form})


@login_required(login_url='users:signin')
@require_http_methods(["GET"])
def my_complaints(request):
    """View user's complaints"""
    complaints = Complaint.objects.filter(user=request.user)
    
    context = {
        'complaints': complaints,
        'open_count': complaints.filter(status='open').count(),
        'resolved_count': complaints.filter(status='resolved').count(),
    }
    return render(request, 'complaints/list.html', context)


@login_required(login_url='users:signin')
@require_http_methods(["GET"])
def complaint_detail(request, complaint_id):
    """View complaint details"""
    complaint = get_object_or_404(Complaint, id=complaint_id, user=request.user)
    return render(request, 'complaints/detail.html', {'complaint': complaint})
