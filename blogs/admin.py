from django.contrib import admin
from .models import Blogs
# Register your models here.

class BlogAdmin(admin.ModelAdmin):
    list_display = ("category","title","sub_desc","description","thumbnail")

admin.site.register(Blogs,BlogAdmin)