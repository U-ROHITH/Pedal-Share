from django.urls import path
from apps.users import views

app_name = 'users'

urlpatterns = [
    path('signin/', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('signout/', views.signout, name='signout'),
    path('profile/', views.profile, name='profile'),
    path('google-callback/', views.google_auth_callback, name='google_callback'),
]
