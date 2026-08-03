from .models import Profile

def is_owner(user, obj):
    return obj.user == user


def is_profile_owner(user, profile):
    return profile.user == user

def get_active_profile(request):
    profile_id = request.session.get("active_profile_id")
    profiles = Profile.objects.filter(user=request.user)

    if profile_id:
        profile = profiles.filter(id=profile_id).first()
        if profile:
            return profile

    if profiles.count() == 1:
        profile = profiles.first()
        request.session["active_profile_id"] = profile.id
        request.session.modified = True
        return profile

    return None
