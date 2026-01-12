from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseForbidden

from .models import Profile, ProfileSection
from .forms import ProfileForm, ProfileSectionForm
from .constants import FREE_PROFILE_LIMIT
from .utils import is_profile_owner


@login_required
def profile_list(request):
    profiles = request.user.profiles.all()
    return render(
        request,
        "profiles/profile_list.html",
        {"profiles": profiles},
    )


@login_required
def profile_create(request):
    if request.user.profiles.count() >= FREE_PROFILE_LIMIT:
        return HttpResponseForbidden("Profile limit reached. Upgrade required.")

    form = ProfileForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        profile = form.save(commit=False)
        profile.user = request.user
        profile.save()
        return redirect("profiles:list")

    return render(request, "profiles/profile_create.html", {"form": form})


@login_required
def section_list_create(request, profile_id):
    profile = get_object_or_404(Profile, id=profile_id, user=request.user)

    sections = profile.sections.all()

    if request.method == "POST":
        form = ProfileSectionForm(request.POST)
        if form.is_valid():
            section = form.save(commit=False)
            section.profile = profile
            section.save()
            return redirect("profiles:sections", profile_id=profile.id)
    else:
        form = ProfileSectionForm()

    return render(
        request,
        "profiles/sections.html",
        {"sections": sections, "form": form, "profile": profile},
    )


def public_profile_view(request, slug):
    profile = get_object_or_404(Profile, slug=slug)

    if profile.visibility == Profile.PRIVATE:
        raise Http404()

    sections = profile.sections.filter(is_enabled=True)

    return render(
        request,
        "profiles/public_profile.html",
        {"profile": profile, "sections": sections},
    )
