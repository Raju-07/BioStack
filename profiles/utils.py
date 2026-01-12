from django.shortcuts import get_object_or_404
from .models import Profile

def is_owner(user, obj):
    return obj.user == user


def is_profile_owner(user, profile):
    return profile.user == user

def get_active_profile(request):
    profile_id = request.session.get("active_profile_id")

    if not profile_id:
        return None

    return get_object_or_404(
        Profile,
        id=profile_id,
        user=request.user,
    )
