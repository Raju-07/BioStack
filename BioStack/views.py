from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.clickjacking import xframe_options_sameorigin

from profiles.forms import FeedbackForm
from accounts.models import UserDetail
from profiles.models import Profile,Theme

class MockImage:
    """Simulates an ImageField file"""
    def __init__(self, url):
        self.url = url

class MockUserDetails:
    """Simulates UserDetail model"""
    def __init__(self):
        # We use a placeholder image for the preview
        self.profile_image = MockImage("https://api.dicebear.com/7.x/avataaars/svg?seed=Felix")

class MockUser:
    """Simulates the User model"""
    def __init__(self):
        self.details = MockUserDetails()
        self.username = "demo_user"

class MockProfile:
    """Simulates the Profile model"""
    def __init__(self, full_name, bio, slug):
        self.full_name = full_name
        self.bio = bio
        self.slug = slug
        self.user = MockUser()
        self.profile_image = None # Use global fallback

class MockSection:
    """Simulates ProfileSection model"""
    def __init__(self, section_type, title, data):
        self.section_type = section_type
        self.title = title
        self.data = data # The JSON data dict
        self.id = 999 # Fake ID for loops

# --- 2. THE VIEWS ---

def templates_view(request):
    """Renders the Gallery Grid"""
    themes = Theme.objects.all().order_by('is_premium') # Show free first, or however you like
    return render(request, 'pages/templates.html', {'themes': themes})

@xframe_options_sameorigin
def theme_preview_view(request, theme_id):
    """
    Renders a specific theme with DUMMY data.
    This allows public users to see what the theme looks like.
    """
    theme = get_object_or_404(Theme, id=theme_id)
    
    # A. Create the Fake Profile
    dummy_profile = MockProfile(
        full_name="Alex Creator",
        bio="Digital Artist & Developer. Building the future of web identity. This is a live preview.",
        slug="alex-demo"
    )
    
    # B. Create Fake Sections (Rich Content for the Demo)
    dummy_sections = [
        MockSection('ABOUT', 'About Me', {
            'content': "I specialize in creating interactive digital experiences. I believe in clean code, accessible design, and pushing the boundaries of what's possible on the web."
        }),
        MockSection('EXPERIENCE', 'Work History', {
            'position': 'Senior Developer', 
            'start_date': '2023-01-01', 
            'end_date': 'Present', 
            'is_current': True,
            'content': 'Leading frontend architecture and design systems for global clients.'
        }),
        MockSection('PROJECTS', 'Neon UI Kit', {
            'content': 'A complete UI library for dark-mode applications. Downloaded by over 10k developers.'
        }),
        MockSection('PROJECTS', 'BioStack App', {
            'content': 'The platform you are looking at right now! Built with Django and Tailwind.'
        }),
        MockSection('SKILLS', 'Tech Stack', {'name': 'Python', 'level': 'Expert'}),
        MockSection('SKILLS', 'Tech Stack', {'name': 'React', 'level': 'Advanced'}),
        MockSection('SKILLS', 'Tech Stack', {'name': 'Figma', 'level': 'Intermediate'}),
        MockSection('LINKS', 'Connect', {'url': 'https://github.com', 'title': 'GitHub'}),
        MockSection('LINKS', 'Connect', {'url': 'https://twitter.com', 'title': 'Twitter/X'}),
        MockSection('PERSONAL', 'Personal Details', {
            'location': 'New York, USA',
            'email': 'alex@example.com',
            'website': 'alex.dev'
        }),
    ]

    # C. Render the ACTUAL theme template (e.g., modern.html) but with fake data
    return render(
        request,
        theme.template_name,
        {"profile": dummy_profile, "sections": dummy_sections}
    )
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
            initial_data = {'name':request.user.details.full_name,'email': request.user.email, }
        form = FeedbackForm(initial=initial_data)

    return render(request, 'navbar/support.html', {'form': form})


def homepage(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thanks for your feedback! We'll look into it.")
            return redirect('home') # Redirects back to clear the form
    else:
        # Pre-fill email if user is logged in
        initial_data = {}
        if request.user.is_authenticated:
            initial_data = {'name':request.user.details.full_name,'email': request.user.email, }
        form = FeedbackForm(initial=initial_data)
    return render(request,'home.html',{'form':form})

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


#views for footer file:
def blog_view(request):
    return render(request,'pages/blog.html')

def career_view(request):
    return render(request,'pages/careers.html')

def privacy_view(request):
    return render(request,'pages/privacy.html')

def showcase_view(request):
    profiles = Profile.objects.filter(visibility='PUBLIC').select_related('user__details').order_by('-created_at')
    return render(request,'pages/showcase.html',{'profiles':profiles})

def terms_view(request):
    return render(request,'pages/terms.html')