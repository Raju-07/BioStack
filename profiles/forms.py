from django import forms
from .models import ProfileSection,Profile


class ProfileSectionForm(forms.ModelForm):
    class Meta:
        model = ProfileSection
        fields = ("section_type", "title", "data", "is_enable", "order")

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("full_name", "bio")
