from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import Http404, HttpResponseForbidden, JsonResponse
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import json

from .models import Profile, ProfileSection,Theme
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
@require_POST
def delete_profile(request, profile_id):
    profile = get_object_or_404(Profile, id=profile_id, user=request.user)

    active_profile_id = request.session.get("active_profile_id")

    if active_profile_id == profile.id:
        messages.error(request, "You cannot delete your currently active profile. Switch to another profile first.")
    else:
        profile.delete()
        messages.success(request, "Profile Deleted Successfully")

    return redirect('profiles:list')
        

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

    #Fetching themes here
    themes =  Theme.objects.all()

    #Ensure profile has a theme (fallback logic)
    if not profile.theme:
        default_theme = Theme.objects.first()
        if default_theme :
            profile_theme = default_theme
            profile.save()
    return render(
        request,
        "profiles/profile_dashboard.html",
        {'profile':profile,'themes':themes},
        content_type='text/html',
    )

# Theme view
@login_required
@require_POST
def update_theme(request):
    profile = get_active_profile(request)
    if not profile:
        return redirect("profile:list")
    
    theme_id = request.POST.get("theme_id")

    #fetching the actual theme object
    theme = get_object_or_404(Theme,id=theme_id)

    profile.theme = theme
    profile.save()

    messages.success(request,f"Theme updated to {theme.name}")
    return redirect("profiles:dashboard")


@login_required
@require_POST
def reorder_sections(request):
    try:
        data = json.loads(request.body)
        order_list = data.get('order', []) # List of IDs [1, 5, 2]
        
        profile = get_active_profile(request)
        if not profile:
            return JsonResponse({'status': 'error'}, status=400)

        # Optimized Approach:
        # Fetch all sections for this profile to memory
        all_sections = {s.id: s for s in profile.sections.all()}
        
        sections_to_update = []
        for index, section_id in enumerate(order_list):
            section = all_sections.get(section_id)
            if section:
                section.order = index
                sections_to_update.append(section)
        
        # Save all at once
        ProfileSection.objects.bulk_update(sections_to_update, ['order'])
                
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

@login_required
def section_list_create(request):
    # 1. Get the active profile
    profile = get_active_profile(request)
    if not profile:
        return redirect("profiles:list")

    # 2. Get existing sections for the list display
    sections = profile.sections.all()

    if request.method == "POST":
        # First, bind the data to a generic form to check the 'section_type'
        form = ProfileSectionForm(request.POST)
        
        if form.is_valid():
            section_type = form.cleaned_data.get("section_type")

            # --- SINGLETON LOGIC (About / Personal) ---
            # If the user is trying to add ABOUT or PERSONAL, check if it already exists.
            if section_type in ['ABOUT', 'PERSONAL']:
                existing_section = profile.sections.filter(section_type=section_type).first()
                
                if existing_section:
                    # UPDATE EXISTING: Re-bind the form with the existing instance
                    form = ProfileSectionForm(request.POST, instance=existing_section)
                    if form.is_valid():
                        section = form.save(commit=False)
                        # Profile is already attached to existing_section, but good to be safe
                        section.save()
                        messages.success(request, f"Updated your {section_type.lower()} section.")
                        return redirect("profiles:sections")

            # --- CREATE NEW LOGIC (Skills, Links, or first-time About) ---
            section = form.save(commit=False)
            section.profile = profile  # <--- CRITICAL: Link to the profile

            # Final safety check for Title (in case Form logic missed it)
            if not section.title:
                if section_type == 'ABOUT':
                    section.title = "About Me"
                elif section_type == 'PERSONAL':
                    section.title = "Personal Details"
                elif section_type == 'SKILLS':
                    # Try to grab skill name from the form data payload if possible, else generic
                    section.title = form.cleaned_data.get('skill_name', 'Skill') 
                else:
                    section.title = "Untitled Section"

            section.save()
            messages.success(request, "Section added successfully.")
            return redirect("profiles:sections")
        
        else:
            # --- DEBUGGING ---
            # If the form is invalid, this prints the exact reason to your Visual Studio Code terminal.
            print("❌ Form Validation Failed:", form.errors)
            messages.error(request, "Please check the form for errors.")

    else:
        # --- NEW LOGIC: Pre-fill from Global User Details ---
        initial_data = {}
        try:
            # Check if the user has global details saved (from the Accounts app)
            if hasattr(request.user, 'details'):
                user_details = request.user.details
                initial_data = {
                    'phone': user_details.phone,
                    'email': request.user.email, # Always use account email
                    'dob': user_details.dob,
                    'gender': user_details.gender,
                    'marital_status': user_details.marital_status,
                    'nationality': user_details.nationality,
                    'address': user_details.address,
                    'location': user_details.location,
                }
        except Exception:
            # If UserDetail table doesn't exist yet or other error, just ignore
            pass

        # Initialize the form with this data (if any)
        form = ProfileSectionForm(initial=initial_data)

    return render(
        request,
        "profiles/sections.html",
        {"sections": sections, "form": form, "profile": profile},
    )

@login_required
@require_POST
def delete_section(request, section_id):
    profile = get_active_profile(request)
    if not profile:
        return redirect("profiles:list")
    
    # Ensure the section belongs to the active profile (Security)
    section = get_object_or_404(ProfileSection, id=section_id, profile=profile)
    section.delete()
    
    messages.success(request, "Section removed successfully.")
    return redirect("profiles:sections")


def public_profile_view(request, slug):
    profile = get_object_or_404(Profile, slug=slug)

    if profile.visibility == Profile.PRIVATE:
        raise Http404()
    
    sections = profile.sections.filter(is_enabled=True)
    
    #logic for dynamic rendering
    if profile.theme:
        template_name = profile.theme.template_name
    else:
        #fallback if db is empty
        template_name = "profiles/themes/modern.html"

    return render(
        request,
        template_name,
        {"profile": profile, "sections": sections},
        content_type="text/html"
    )