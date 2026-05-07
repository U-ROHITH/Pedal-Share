import os
from apps.users.models import UserProfile

def user_profile(request):
    """
    Context processor to provide global data to templates:
    - GOOGLE_OAUTH_CLIENT_ID: for Google Login
    - user_profile: UserProfile object for the logged in user
    """
    ctx = {
        'GOOGLE_OAUTH_CLIENT_ID': os.environ.get('GOOGLE_OAUTH_CLIENT_ID', '')
    }
    if request.user.is_authenticated:
        # Get or create profile for authenticated users
        profile, _ = UserProfile.objects.get_or_create(user=request.user)
        ctx['user_profile'] = profile
    else:
        ctx['user_profile'] = None
    return ctx
