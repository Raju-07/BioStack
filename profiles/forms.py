from django import forms
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from .models import ProfileSection, Profile,Feedback

User = get_user_model()
class ProfileSectionForm(forms.ModelForm):
    # --- 1. General Content Field ---
    content = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows': 4, 'placeholder': 'Write your details here...'}),
        label="Description / Bio",
        help_text="Main text content for this section."
    )
    title = forms.CharField(
        required=False,
        label="Title / Heading",
        max_length=255,
        widget=forms.TextInput(attrs={'placeholder': 'Section Title'})
    )

    # --- 2. Link Specific Fields ---
    link_url = forms.URLField(
        required=False,
        label="Destination URL",
        widget=forms.URLInput(attrs={'placeholder': 'https://example.com'})
    )

    # --- 3. Experience Specific Fields ---
    position = forms.CharField(
        required=False,
        label="Job Title / Role",
        max_length=100
    )
    start_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'}),
        label="Start Date"
    )
    end_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'}),
        label="End Date"
    )
    is_current = forms.BooleanField(
        required=False,
        label="I currently work here",
        initial=False
    )

    # --- 4. Skill Specific Fields ---
    skill_name = forms.CharField(
        required=False, 
        label="Skill Name",
        max_length=100,
        help_text="e.g. Python, UI Design"
    )
    skill_level = forms.ChoiceField(
        choices=[
            ("Beginner", "Beginner"), 
            ("Intermediate", "Intermediate"), 
            ("Advanced", "Advanced"), 
            ("Expert", "Expert")
        ],
        required=False, 
        label="Proficiency"
    )

    profile_image = forms.ImageField(required=False,label="Profile Photo",
        widget=forms.FileInput(attrs={'class': 'hidden', 'id': 'id_profile_image'}))

    # --- 5. Personal Details Fields (UPDATED) ---
    phone = forms.CharField(required=False, label="Phone Number", max_length=50)
    email = forms.EmailField(required=False, label="Email Address")
    dob = forms.DateField(required=False, label="Date of Birth", widget=forms.DateInput(attrs={'type': 'date'}))
    gender = forms.ChoiceField(
        choices=[("Male", "Male"), ("Female", "Female"), ("Other", "Other")],
        required=False, label="Gender"
    )
    marital_status = forms.ChoiceField(
        choices=[("Single", "Single"), ("Married", "Married"), ("Divorced", "Divorced")],
        required=False, label="Marital Status"
    )
    nationality = forms.CharField(required=False, label="Nationality", max_length=100)
    address = forms.CharField(required=False, label="Address", widget=forms.Textarea(attrs={'rows': 2}))
    location = forms.CharField(required=False, label="City / Location", max_length=100)


    class Meta:
        model = ProfileSection
        fields = ("section_type", "title", "is_enabled")
        labels = {
            "title": "Title / Heading",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        if self.instance and self.instance.pk and self.instance.data:
            data = self.instance.data
            
            # Unpack JSON data into fields
            self.fields['content'].initial = data.get('content', '')
            self.fields['link_url'].initial = data.get('url', '')
            self.fields['position'].initial = data.get('position', '')
            self.fields['start_date'].initial = data.get('start_date', '')
            self.fields['end_date'].initial = data.get('end_date', '')
            self.fields['is_current'].initial = data.get('is_current', False)
            self.fields['skill_name'].initial = data.get('name', '')
            self.fields['skill_level'].initial = data.get('level', '')
            
            # Personal Data Unpacking
            self.fields['phone'].initial = data.get('phone', '')
            self.fields['email'].initial = data.get('email', '')
            self.fields['dob'].initial = data.get('dob', '')
            self.fields['gender'].initial = data.get('gender', '')
            self.fields['marital_status'].initial = data.get('marital_status', '')
            self.fields['nationality'].initial = data.get('nationality', '')
            self.fields['address'].initial = data.get('address', '')
            self.fields['location'].initial = data.get('location', '')

    def clean(self):
        cleaned_data = super().clean()
        section_type = cleaned_data.get("section_type")

        if section_type == "LINKS" and not cleaned_data.get("link_url"):
            self.add_error("link_url", "URL is required for Link sections.")
        
        if section_type == "EXPERIENCE":
            if not cleaned_data.get("position"):
                self.add_error("position", "Job Title is required.")
            if not cleaned_data.get("start_date"):
                self.add_error("start_date", "Start Date is required.")

        if section_type == "SKILLS" and not cleaned_data.get("skill_name"):
             self.add_error("skill_name", "Skill Name is required.")

        return cleaned_data

    def save(self, commit=True):
        section = super().save(commit=False)
        section_type = self.cleaned_data.get("section_type")
        
        json_payload = {}

        if section_type == "LINKS":
            json_payload = {
                "url": self.cleaned_data.get("link_url"),
                "content": self.cleaned_data.get("content")
            }

        elif section_type == "EXPERIENCE":
            s_date = self.cleaned_data.get("start_date")
            e_date = self.cleaned_data.get("end_date")
            is_curr = self.cleaned_data.get("is_current")
            json_payload = {
                "position": self.cleaned_data.get("position"),
                "start_date": s_date.isoformat() if s_date else None,
                "end_date": e_date.isoformat() if e_date and not is_curr else None,
                "is_current": is_curr,
                "content": self.cleaned_data.get("content")
            }

        # --- FIX: Added 'content' to Skills ---
        elif section_type == "SKILLS":
            json_payload = {
                "name": self.cleaned_data.get("skill_name"),
                "level": self.cleaned_data.get("skill_level"),
                "content": self.cleaned_data.get("content") # <--- ADDED THIS
            }
            if self.cleaned_data.get("skill_name"):
                section.title = self.cleaned_data.get("skill_name")

        # --- FIX: Updated Personal Details ---
        elif section_type == "PERSONAL":
            json_payload = {
                "phone": self.cleaned_data.get("phone"),
                "email": self.cleaned_data.get("email"),
                "dob": str(self.cleaned_data.get("dob")) if self.cleaned_data.get("dob") else "",
                "gender": self.cleaned_data.get("gender"),
                "marital_status": self.cleaned_data.get("marital_status"),
                "nationality": self.cleaned_data.get("nationality"),
                "address": self.cleaned_data.get("address"),
                "location": self.cleaned_data.get("location"),
                "content": self.cleaned_data.get("content")
            }
            section.title = "Personal Details"

        elif section_type == "ABOUT":
            json_payload = {
                "content": self.cleaned_data.get("content")
            }
            if not section.title:
                section.title = "About Me"

        else:
            json_payload = {
                "content": self.cleaned_data.get("content")
            }

        section.data = json_payload

        if commit:
            section.save()
        return section

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("full_name", "bio", "slug", "visibility")

        widgets = {
            'full_name': forms.TextInput(attrs={
                'placeholder': 'e.g. Raju Yadav',
                'class': 'w-full bg-[#0F172A] border border-white/10 rounded-xl px-4 py-3 text-slate-200 focus:outline-none focus:border-indigo-500 transition placeholder-slate-500'
            }),
            'bio': forms.Textarea(attrs={
                'placeholder': 'Tell the world a little about yourself...',
                'rows': 4,
                'class': 'w-full bg-[#0F172A] border border-white/10 rounded-xl px-4 py-3 text-slate-200 focus:outline-none focus:border-indigo-500 transition placeholder-slate-500 resize-none'
            }),
            'slug': forms.TextInput(attrs={
                'placeholder': 'my-custom-handle',
                'class': 'w-full bg-[#0F172A] border border-white/10 rounded-xl px-4 py-3 text-slate-200 focus:outline-none focus:border-indigo-500 transition placeholder-slate-500'
            }),
            'visibility': forms.Select(attrs={
                'class': 'w-full bg-[#0F172A] border border-white/10 rounded-xl px-4 py-3 text-slate-200 focus:outline-none focus:border-indigo-500 transition cursor-pointer'
            }),
        }
        labels = {
            "full_name": "Display Name",
            "slug": "Profile URL Handle",
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None) # Extract user from kwargs
        super().__init__(*args, **kwargs)

        if self.user:
            try:
                # Access subscription safely
                if not hasattr(self.user, 'subscription') or not self.user.subscription.is_pro:
                    if 'slug' in self.fields:
                        del self.fields['slug']
            except Exception:

                if 'slug' in self.fields:
                    del self.fields['slug']

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full bg-[#0F172A] border border-white/10 rounded-xl px-4 py-3 text-slate-200 focus:outline-none focus:border-indigo-500 transition placeholder-slate-500',
                'placeholder': 'Your Name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full bg-[#0F172A] border border-white/10 rounded-xl px-4 py-3 text-slate-200 focus:outline-none focus:border-indigo-500 transition placeholder-slate-500',
                'placeholder': 'your@email.com'
            }),
            'subject': forms.Select(attrs={
                'class': 'w-full bg-[#0F172A] border border-white/10 rounded-xl px-4 py-3 text-slate-200 focus:outline-none focus:border-indigo-500 transition cursor-pointer'
            }),
            'message': forms.Textarea(attrs={
                'class': 'w-full bg-[#0F172A] border border-white/10 rounded-xl px-4 py-3 text-slate-200 focus:outline-none focus:border-indigo-500 transition placeholder-slate-500 h-32 resize-none',
                'placeholder': 'How can we improve BioStack?'
            }),
        }

class UserUpdateForm(forms.ModelForm):
    username = forms.CharField(
        validators=[
            RegexValidator(
                regex=r'^[\w-]+$',
                message='Username can only contain letters, numbers, underscores, and hyphens (no spaces).',
                code='invalid_username'
            )
        ],
        widget=forms.TextInput(attrs={
            'class': 'w-full bg-slate-900/50 border border-white/10 rounded-xl px-4 py-3 text-white focus:border-indigo-500 focus:outline-none transition',
            'placeholder': 'username'
        })
    )

    class Meta:
        model = User
        fields = ['username']

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        if User.objects.filter(username=username).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("This username is already taken.")
        return username

class ProfileUpdateForm(forms.ModelForm):
    slug = forms.SlugField(
        widget=forms.TextInput(attrs={
            'class': 'flex-1 bg-transparent px-4 py-3 text-white focus:outline-none placeholder-slate-600',
            'placeholder': 'slug'
        })
    )
    
    class Meta:
        model = Profile
        fields = ['full_name', 'slug', 'bio',]