from django.contrib import admin
from .models import Profile,Theme,Feedback


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "full_name", "created_at")
    search_fields = ("user__email", "full_name")

@admin.register(Theme)
class ThemeAdmin(admin.ModelAdmin):
    list_display = ('name','template_name','is_premium')
    prepopulated_fields = {'slug':('name',)}
    list_filter = ('is_premium',)

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ("name","email","subject","message","created_at")
    search_fields = ('name','email','subject','created_at')
    list_filter = ('email','created_at','subject')

