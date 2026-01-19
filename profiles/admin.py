from django.contrib import admin
from .models import Profile,Theme,ProfileSection


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "full_name", "created_at")
    search_fields = ("user__email", "full_name")

@admin.register(Theme)
class ThemeAdmin(admin.ModelAdmin):
    list_display = ('name','template_name','is_premium')
    prepopulated_fields = {'slug':('name',)}

