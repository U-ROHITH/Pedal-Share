from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from apps.users.forms import SignUpForm, SignInForm, UserProfileForm
from apps.users.models import UserProfile
import json
import os


@require_http_methods(["GET", "POST"])
def signin(request):
    """Handle user sign in"""
    if request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            # Try to authenticate with username or email
            user = authenticate(request, username=username, password=password)
            if user is None:
                try:
                    user_obj = User.objects.get(email=username)
                    user = authenticate(request, username=user_obj.username, password=password)
                except User.DoesNotExist:
                    pass
            
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.username}!')
                return redirect('home')
            else:
                messages.error(request, 'Invalid username/email or password.')
    else:
        form = SignInForm()
    
    return render(request, 'auth/signin.html', {'form': form})


@require_http_methods(["GET", "POST"])
def signup(request):
    """Handle user registration"""
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('home')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = SignUpForm()
    
    return render(request, 'auth/signup.html', {'form': form})


@login_required(login_url='users:signin')
@require_http_methods(["GET"])
def signout(request):
    """Handle user sign out"""
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('home')


@login_required(login_url='users:signin')
@require_http_methods(["GET", "POST"])
def profile(request):
    """Handle user profile view and update"""
    profile = request.user.profile
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=profile)
    
    return render(request, 'auth/profile.html', {'form': form, 'profile': profile})


@csrf_exempt
@require_http_methods(["POST"])
def google_auth_callback(request):
    """Handle Google Sign-In callback — verify ID token and log user in.
    Supports both JSON (popup mode) and form-encoded (redirect mode) POST.
    """
    try:
        from google.oauth2 import id_token
        from google.auth.transport import requests as google_requests

        # Get credential from either JSON body or form data
        content_type = request.content_type or ''
        is_json = 'application/json' in content_type

        if is_json:
            body = json.loads(request.body)
            credential = body.get('credential', '')
        else:
            # Google redirect mode sends form-encoded data
            credential = request.POST.get('credential', '')

        if not credential:
            if is_json:
                return JsonResponse({'error': 'No credential provided'}, status=400)
            else:
                messages.error(request, 'Google sign-in failed: no credential received.')
                return redirect('users:signin')

        client_id = os.environ.get('GOOGLE_OAUTH_CLIENT_ID', '')
        idinfo = id_token.verify_oauth2_token(
            credential,
            google_requests.Request(),
            client_id,
        )

        email = idinfo.get('email', '')
        first_name = idinfo.get('given_name', '')
        last_name = idinfo.get('family_name', '')

        if not email:
            if is_json:
                return JsonResponse({'error': 'Email not provided by Google'}, status=400)
            else:
                messages.error(request, 'Google sign-in failed: email not provided.')
                return redirect('users:signin')

        # Find or create user
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            # Create a username from email prefix
            base_username = email.split('@')[0]
            username = base_username
            counter = 1
            while User.objects.filter(username=username).exists():
                username = f'{base_username}{counter}'
                counter += 1

            user = User.objects.create_user(
                username=username,
                email=email,
                first_name=first_name,
                last_name=last_name,
            )
            user.set_unusable_password()
            user.save()

        # Ensure profile exists
        UserProfile.objects.get_or_create(user=user)

        login(request, user)
        messages.success(request, f'Welcome, {user.first_name or user.username}!')

        if is_json:
            return JsonResponse({'success': True, 'redirect': '/'})
        else:
            return redirect('home')

    except ValueError as e:
        if is_json:
            return JsonResponse({'error': f'Invalid token: {str(e)}'}, status=400)
        else:
            messages.error(request, f'Google sign-in failed: invalid token.')
            return redirect('users:signin')
    except Exception as e:
        if is_json:
            return JsonResponse({'error': f'Server error: {str(e)}'}, status=500)
        else:
            messages.error(request, 'Google sign-in failed. Please try again.')
            return redirect('users:signin')
