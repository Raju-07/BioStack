from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from profiles.forms import FeedbackForm

from accounts.models import UserDetail

@login_required
def support(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thanks for your feedback! We'll look into it.")
            return redirect('support') # Redirects back to clear the form
    else:
        # Pre-fill email if user is logged in
        initial_data = {}
        if request.user.is_authenticated:
            initial_data = {'email': request.user.email, }
        form = FeedbackForm(initial=initial_data)

    return render(request, 'navbar/support.html', {'form': form})


def homepage(request):
    return render(request,'home.html')

def pricing(request):
    return render(request,'navbar/pricing.html')

def about_view(request):
    return render(request,'navbar/about.html')

def features_view(request):
    return render(request,'navbar/features.html')

@login_required
def test(request):
    user_details = None
    if hasattr(request.user,'details'):
        user_details = request.user.userdetails
    return render(request,'test.html',{"my_details":user_details})