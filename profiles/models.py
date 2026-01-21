from django.db import models
from django.conf import settings
from django.db.models import UniqueConstraint,Q
from django.utils.text import slugify


    
# Model for theme
class Theme(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    #path to the template
    template_name = models.CharField(max_length=255)

    #preview Image for Dashbaord
    thumbnail = models.ImageField(upload_to="theme_thumbnails/",blank=True,null=True)

    #for premium
    is_premium = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    

class Profile(models.Model):
    PUBLIC = "PUBLIC"
    PRIVATE = "PRIVATE"

    VISIBILITY_CHOICES = [
        (PUBLIC, "Public"),
        (PRIVATE, "Private"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profiles", 
    )

# Profile Image 
    profile_image = models.ImageField(upload_to="profile_images/",blank=True,null=True)

    full_name = models.CharField(max_length=255, blank=True)
    bio = models.TextField(blank=True)

    slug = models.SlugField(max_length=150)
    visibility = models.CharField(
        max_length=10,
        choices=VISIBILITY_CHOICES,
        default=PRIVATE,
    )
# linking the theme to the account
    theme = models.ForeignKey(Theme,on_delete=models.SET_NULL,null=True,related_name="profiles")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [ models.UniqueConstraint(fields=['user', 'slug'],name='unique_user_profile_slug')]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.full_name or "profile")
            base = self.slug
            counter = 1
            while Profile.objects.filter(user=self.user,slug = self.slug).exists():
                self.slug = f"{base}-{counter}"
                counter += 1
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.slug} ({self.visibility})"


class ProfileSection(models.Model):
    # Section Types
    ABOUT = "ABOUT"
    SKILLS = "SKILLS"
    LINKS = "LINKS"
    PROJECTS = "PROJECTS"
    EXPERIENCE = "EXPERIENCE"
    PERSONAL = "PERSONAL" 
    CUSTOM = "CUSTOM"

    SECTION_TYPES = [
        (ABOUT, "About Me"),
        (SKILLS, "Skills"),
        (LINKS, "Links"),
        (PROJECTS, "Projects"),
        (EXPERIENCE, "Experience"),
        (PERSONAL, "Personal Details"),
        (CUSTOM, "Custom Section"),
    ]

    profile = models.ForeignKey(
        'Profile', # Assuming Profile is in the same app
        on_delete=models.CASCADE,
        related_name="sections",
    )

    section_type = models.CharField(max_length=20, choices=SECTION_TYPES)
    title = models.CharField(max_length=255)
    
    # We store all data here. 
    # For About: {"content": "..."}
    # For Skills: {"name": "Python", "level": "Expert"}
    data = models.JSONField(default=dict)

    is_enabled = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order", "created_at"]
        constraints = [
            # CONSTRAINT 1: Only ONE 'About' section per profile
            UniqueConstraint(
                fields=['profile', 'section_type'],
                condition=Q(section_type='ABOUT'),
                name='unique_about_section'
            ),
            # CONSTRAINT 2: Only ONE 'Personal Details' section per profile
            UniqueConstraint(
                fields=['profile', 'section_type'],
                condition=Q(section_type='PERSONAL'),
                name='unique_personal_section'
            )
        ]

    def __str__(self):
        return f"{self.section_type} - {self.title}"

class Feedback(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200, choices=[
        ('suggestion', 'Suggestion'),
        ('bug', 'Bug Report'),
        ('other', 'Other')
    ], default='suggestion')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"
    
# Creating model for Implimenting Analytics

class ProfileView(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='views')
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

class LinkClick(models.Model):
    profile_section = models.ForeignKey(ProfileSection, on_delete=models.CASCADE, related_name='clicks')
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']