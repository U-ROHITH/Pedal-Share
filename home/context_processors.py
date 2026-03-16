from apps.users.models import UserProfile
import os


def user_profile(request):
    ctx = {
        'GOOGLE_OAUTH_CLIENT_ID': os.environ.get('GOOGLE_OAUTH_CLIENT_ID', '')
    }
    if request.user.is_authenticated:
        profile, _ = UserProfile.objects.get_or_create(user=request.user)
        ctx['user_profile'] = profile
    else:
        ctx['user_profile'] = None
    return ctx
