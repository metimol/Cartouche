from .models import *

def profile_check(user):
    if not user.is_authenticated:
        return True
    try:
        profile = Profile.objects.get(user=user)
        return True
    except:
        return False