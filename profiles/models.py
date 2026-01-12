from django.db import models
from django.conf import settings
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
    ABOUT = "ABOUT"
    SKILLS = "SKILLS"
    LINKS = "LINKS"
    PROJECTS = "PROJECTS"
    EXPERIENCE = "EXPERIENCE"

    SECTION_TYPES = [
        (ABOUT, "About"),
        (SKILLS, "Skills"),
        (LINKS, "Links"),
        (PROJECTS, "Projects"),
        (EXPERIENCE, "Experience"),
    ]

    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name="sections",
    )

    section_type = models.CharField(max_length=20, choices=SECTION_TYPES)
    title = models.CharField(max_length=255)
    data = models.JSONField(default=dict)

    is_enabled = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order", "created_at"]
        unique_together = ("profile", "section_type")

    def __str__(self):
        return f"{self.section_type} ({self.profile.slug})"
