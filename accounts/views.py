from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import SignupForm, LoginForm,UserDetailForm
from .models import UserDetail


def signup_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard:index")

    form = SignupForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        return redirect("dashboard:index")

    return render(request, "accounts/signup.html", {"form": form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard:index")

    form = LoginForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        login(request, form.cleaned_data["user"])
        return redirect("dashboard:index")

    return render(request, "accounts/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("accounts:login")

@login_required
def user_details(request):
    # Ensure the user has a UserDetail object (failsafe for old users)
    if not hasattr(request.user, 'details'):
        UserDetail.objects.create(user=request.user)

    if request.method == 'POST':
        form = UserDetailForm(request.POST, request.FILES, instance=request.user.details)
        
        if form.is_valid():
            form.save()
            messages.success(request, "Global personal details updated successfully.")
            return redirect('accounts:userdetails')
            
        else:
            # --- CHANGE IS HERE ---
            # If the form is invalid (e.g., file too big), catch the error
            if 'profile_image' in form.errors:
                # Get the specific error message from forms.py (e.g., "The image file is too large")
                error_msg = form.errors['profile_image'][0]
                messages.error(request, f"Upload Failed: {error_msg}")
            else:
                # Handle other form errors (like invalid phone number, etc.)
                messages.error(request, "Please correct the errors below.")
                
    else:
        form = UserDetailForm(instance=request.user.details)

    return render(request, 'accounts/userdetails.html', {'form': form})
