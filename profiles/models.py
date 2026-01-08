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

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
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
            self.slug = slugify(self.user.email.split("@")[0])
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.slug} ({self.visibility})"
