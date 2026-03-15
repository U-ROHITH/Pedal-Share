from django.shortcuts import render, HttpResponse

# Create your views here.
def base(request):
    return render(request, 'base.html')

def signin(request):
    return render(request, 'signin.html')

def signup(request):
    return render(request, 'signup.html')

def aboutus(request):
    return render(request, 'aboutus.html')

def contactus(request):
     return render(request, 'contactus.html')

def availablecycles(request):
     return render(request, 'availablecycles.html') 

def contact(request):
    return HttpResponse("this is about page contact us")

def frontend(request):
    return render(request, 'frontend.html') 

def wallet(request):
    return render(request, 'wallet.html')

def PaymentGateway(request):
    return render(request, 'PaymentGateway.html')