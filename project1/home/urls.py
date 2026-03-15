from django.contrib import admin
from django.urls import path
from home import views
from django.shortcuts import render

urlpatterns = [
    path("",views.base, name = 'base'),
    path("frontend.html",views.frontend, name = 'home'),
    path("base.html",views.base, name = 'index'),
    path("aboutus.html",views.aboutus, name = 'aboutus'),
   # path("services",views.services, name = 'services'),
    path("signin.html",views.signin, name = 'Sign In'),
    path("signup.html",views.signup, name = 'Sign Up'),
    path("availablecycles.html",views.availablecycles, name = 'Sign Up'),
    path("contactus.html",views.contactus ,name='contactus'),
    path("wallet.html",views.wallet ,name='wallet'),
    path("PaymentGateway.html", views.PaymentGateway , name = "payment gateway")

]


