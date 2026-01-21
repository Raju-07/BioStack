from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import Http404, HttpResponseForbidden, JsonResponse
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta

from .models import Profile, ProfileSection,Theme,ProfileView,LinkClick
from .forms import ProfileForm, ProfileSectionForm
from .constants import FREE_PROFILE_LIMIT
from .utils import get_active_profile


# (Helper Function ) getting Ip address
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


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

    messages.success(request,f'Profile changed')
    return redirect(reverse("profiles:list"))


@login_required
def theme_store(request):
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
    return redirect("profiles:themes")


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
        # Bind the form initially
        form = ProfileSectionForm(request.POST, request.FILES)
        
        if form.is_valid():
            section_type = form.cleaned_data.get("section_type")

            # --- 1. IMAGE HANDLING (Profile Level) ---
            if section_type == 'PERSONAL':
                uploaded_image = request.FILES.get('profile_image')
                if uploaded_image:
                    profile.profile_image = uploaded_image
                    profile.save()

            # --- 2. DETERMINE IF UPDATE OR CREATE ---
            existing_section = None
            if section_type in ['ABOUT', 'PERSONAL']:
                existing_section = profile.sections.filter(section_type=section_type).first()
            
            # --- 3. EXECUTE LOGIC ---
            if existing_section:
                # === UPDATE PATH ===
                # Re-bind form to the existing instance
                form = ProfileSectionForm(request.POST, request.FILES, instance=existing_section)
                
                if form.is_valid():
                    section = form.save(commit=False)
                    section.save()
                    messages.success(request, f"Updated your {section_type.lower()} section.")
                    return redirect("profiles:sections")
                
                # If form is INVALID, we do nothing here. 
                # The code falls through to the 'render' at the bottom, which displays the errors.

            else:
                # === CREATE PATH ===
                # Only run this if we are NOT updating an existing section
                section = form.save(commit=False)
                section.profile = profile

                # Title Logic
                if not section.title:
                    if section_type == 'ABOUT':
                        section.title = "About Me"
                    elif section_type == 'PERSONAL':
                        section.title = "Personal Details"
                    elif section_type == 'SKILLS':
                        section.title = form.cleaned_data.get('skill_name', 'Skill') 
                    else:
                        section.title = "Untitled Section"

                section.save()
                messages.success(request, "Section added successfully.")
                return redirect("profiles:sections")
        
        else:
            print("❌ Form Validation Failed:", form.errors)
            messages.error(request, "Please check the form for errors.")

    else:
        # Pre-fill logic (same as before)
        initial_data = {}
        try:
            if hasattr(request.user, 'details'):
                user_details = request.user.details
                initial_data = {
                    'phone': user_details.phone,
                    'email': request.user.email,
                    'dob': user_details.dob,
                    'gender': user_details.gender,
                    'marital_status': user_details.marital_status,
                    'nationality': user_details.nationality,
                    'address': user_details.address,
                    'location': user_details.location,
                }
        except Exception:
            pass

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

User = get_user_model()
def public_profile_view(request,username, profile_slug):
    user_obj = get_object_or_404(User,username=username)
    profile = get_object_or_404(Profile, user = user_obj, slug=profile_slug)

    if profile.visibility == Profile.PRIVATE:
        raise Http404()
    
    sections = profile.sections.filter(is_enabled=True)

# implimenting Analytics logic 
    session_key = f"profile_view_{profile.id}"
    if not request.session.get("session_key"):
        ProfileView.objects.create(profile=profile,ip_address=get_client_ip(request))
        request.session[session_key] = True
        request.session.set_expiry(60*30)  # Expiry in 30 minutes
    

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

# View for tracking link clicks

def track_link_click(request,section_id):
    section = get_object_or_404(ProfileSection,id = section_id)
    #capturing the click
    LinkClick.objects.create(profile_section=section)

    target_url = section.data.get('url','#')
    return redirect(target_url)
