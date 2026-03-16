from django.shortcuts import render
from django.views.decorators.http import require_http_methods


# All functionality has been moved to modular apps for better organization

@require_http_methods(['GET'])
def frontend(request):
    '''Render home page (landing page)'''
    return render(request, 'home.html')


@require_http_methods(['GET'])
def base(request):
    '''Render base template'''
    return render(request, 'base.html')
