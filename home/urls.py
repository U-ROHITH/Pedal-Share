from django.urls import path
from home import views

urlpatterns = [
    # Home pages
    path("", views.frontend, name='home'),
    path("base/", views.base, name='base'),
]
