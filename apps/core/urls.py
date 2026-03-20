from django.urls import path
from django.views.generic import TemplateView
from django.views.decorators.http import require_http_methods
from django.shortcuts import render
from django.contrib import messages

app_name = 'pages'

def contactus_view(request):
    """Handle contact us page - both GET (show form) and POST (submit form)"""
    if request.method == 'POST':
        fullname = request.POST.get('fullname', '')
        email = request.POST.get('email', '')
        subject = request.POST.get('subject', '')
        message_text = request.POST.get('message', '')
        
        if fullname and email and subject and message_text:
            messages.success(request, 'Thank you for your message! We\'ll get back to you within 24 hours.')
        else:
            messages.error(request, 'Please fill in all fields.')
    
    return render(request, 'pages/contactus.html')

urlpatterns = [
    path('help/', TemplateView.as_view(template_name='pages/help.html'), name='help'),
    path('about/', TemplateView.as_view(template_name='pages/aboutus.html'), name='aboutus'),
    path('contact/', contactus_view, name='contactus'),
]
