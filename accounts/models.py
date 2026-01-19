import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db.models.signals import post_save
from django.dispatch import receiver
from .managers import UserManager

class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

# --- NEW ADDITION BELOW ---

class UserDetail(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='details')
    
    # Personal Fields
    full_name = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    dob = models.DateField(null=True, blank=True, verbose_name="Date of Birth")
    gender = models.CharField(max_length=20, choices=[
        ("Male", "Male"), ("Female", "Female"), ("Other", "Other")
    ], blank=True)
    marital_status = models.CharField(max_length=20, choices=[
        ("Single", "Single"), ("Married", "Married"), ("Divorced", "Divorced")
    ], blank=True)
    nationality = models.CharField(max_length=100, blank=True)
    address = models.TextField(blank=True)
    location = models.CharField(max_length=100, blank=True, help_text="City/State")

    def __str__(self):
        return f"Details for {self.user.email}"

# Signals to auto-create UserDetail when User is created
@receiver(post_save, sender=User)
def create_user_detail(sender, instance, created, **kwargs):
    if created:
        UserDetail.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_detail(sender, instance, **kwargs):
    instance.details.save()