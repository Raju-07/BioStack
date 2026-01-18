from django.shortcuts import render, redirect
from profiles.models import Profile
import json

def dashboard_view(request):
    profile_id = request.session.get("active_profile_id")
    
    profile = None
    if profile_id:
        profile = Profile.objects.filter(id=profile_id, user=request.user).first()

    if not profile:
        return redirect("profiles:list")

    context = {
        "profile": profile,
        "stats": {
            "views": 0,
            "clicks": 0,
        },
        "chart_data": json.dumps([15, 22, 18, 30, 25, 45, 55]),  # temporary
    }

    return render(request, "dashboard/index.html", context)

    

# Create your views here.
