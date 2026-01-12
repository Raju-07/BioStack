def is_owner(user, obj):
    return obj.user == user


def is_profile_owner(user, profile):
    return profile.user == user
