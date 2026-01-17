from django.db import models
from django.conf import settings
from django.db.models import UniqueConstraint,Q
from django.utils.text import slugify


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

    full_name = models.CharField(max_length=255, blank=True)
    bio = models.TextField(blank=True)

    slug = models.SlugField(unique=True, max_length=150)
    visibility = models.CharField(
        max_length=10,
        choices=VISIBILITY_CHOICES,
        default=PRIVATE,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.user.email.split("@")[0])
            slug = base
            counter = 1
            while Profile.objects.filter(slug=slug).exists():
                slug = f"{base}-{counter}"
                counter += 1
            self.slug = slug
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
