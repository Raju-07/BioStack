from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .forms import ProfileForm


@login_required
def profile_view(request):
    profile = request.user.profile

    form = ProfileForm(request.POST or None, instance=profile)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("dashboard:index")

    return render(request, "profiles/profile.html", {"form": form})
