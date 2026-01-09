from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import Http404

from .forms import ProfileForm,ProfileSectionForm
from .models import ProfileSection,Profile
from .utils import is_profile_owner



@login_required
def profile_view(request):
    profile = request.user.profile

    form = ProfileForm(request.POST or None, instance=profile)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("dashboard:index")

    return render(request, "profiles/profile.html", {"form": form})

@login_required
def section_list_create(request):
    profile = request.user.profile

    if not is_profile_owner(request.user,profile):
        raise Http404()
    
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

    return render(request,"profiles/sections.html",{"sections":sections,"form":form})

@login_required
def section_edit(request,section_id):
    section = get_object_or_404(ProfileSection,id=section_id)
    profile = section.profile

    if not is_profile_owner(request.user,profile):
        raise Http404()
    
    form = ProfileSectionForm(request.POST or None, instance=section)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("profiles:sections")
    
    return render(request,"profiles/section_edit",{"form":form},)


def public_profile_view(request,slug):
    profile = get_object_or_404(Profile,slug=slug)

    if profile.visibility == Profile.PRIVATE:
        raise Http404("Profile not Found or set to private")
    
    sections = profile.sections.filter(is_enable = True)

    return render(request,"profiles/public_profile.html",{"profile":profile,"sections":sections},)

