from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseForbidden
from django.urls import reverse

from .models import Profile, ProfileSection
from .forms import ProfileForm, ProfileSectionForm
from .constants import FREE_PROFILE_LIMIT
from .utils import get_active_profile


@login_required
def profile_list(request):
    profiles = request.user.profiles.all()
    active_profile_id = request.session.get("active_profile_id")

    return render(
        request,
        "profiles/profile_list.html",
        {
            "profiles": profiles,
            "active_profile_id": active_profile_id,
        },
    )


@login_required
def profile_create(request):
    if request.user.profiles.count() >= FREE_PROFILE_LIMIT:
        return HttpResponseForbidden("Profile limit reached.")

    form = ProfileForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        profile = form.save(commit=False)
        profile.user = request.user
        profile.save()
        return redirect("profiles:list")

    return render(request, "profiles/profile_create.html", {"form": form})


@login_required
def set_active_profile(request, profile_id):
    profile = get_object_or_404(
        Profile,
        id=profile_id,
        user=request.user,
    )

    request.session["active_profile_id"] = profile.id
    request.session.modified = True  # CRITICAL

    return redirect(reverse("profiles:dashboard"))


@login_required
def profile_dashboard(request):
    profile = get_active_profile(request)

    if not profile:
        return redirect("profiles:list")

    return render(
        request,
        "profiles/profile_dashboard.html",
        {"profile": profile},
    )


@login_required
def section_list_create(request):
    profile = get_active_profile(request)

    if not profile:
        return redirect("profiles:list")

    sections = profile.sections.all()

    if request.method == "POST":
        form = ProfileSectionForm(request.POST)
        if form.is_valid():
            section = form.save(commit=False)
            section.profile = profile
            section.save()
            return redirect("profiles:sections")
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
