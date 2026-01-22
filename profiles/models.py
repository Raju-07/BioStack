from django.db import models
from django.conf import settings
from django.db.models import UniqueConstraint,Q
from django.utils.text import slugify
from django.utils import timezone
import secrets

    
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
            if self.full_name:
                base_slug = slugify(self.full_name)
            else:
                base_slug = "user-biostack"
            
            if Profile.objects.filter(slug = base_slug).exists():
                random_suffix = secrets.urlsafe(4).lower()
                self.slug = f"{base_slug}-{random_suffix}"
            else:
                self.slug = base_slug
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

#model for subscription 

class Subscription(models.Model):
    PLAN_CHOICE = (
        ('FREE', 'Free Plan'),
        ('MONTHLY', 'Pro Monthly'),
        ('YEARLY', 'Pro Yearly')
    )
    
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='subscription')
    plan_type = models.CharField(
        max_length=20, 
        choices=PLAN_CHOICE,   
        default='FREE',        
        blank=True, 
        null=True
    )
    
    is_active = models.BooleanField(default=True)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True, blank=True)
    stripe_subscription_id = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        plan_display = self.get_plan_type_display() if self.plan_type else "No Plan"
        return f"{self.user.username} - {plan_display}"
    
    @property
    def is_pro(self):
        if not self.plan_type or self.plan_type == 'FREE':
            return False
        
        if self.end_date and timezone.now() > self.end_date:
            return False
        
        return True