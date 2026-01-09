from django.urls import path
from .views import profile_view,section_edit,public_profile_view,section_list_create

app_name = "profiles"

urlpatterns = [
    path("me/", profile_view, name="me"),
    path("me/sections/",section_list_create,name='sections'),
    path("me/sections/<int:section_id>/edit/",section_edit,name='section_edit'),
    path("<slug:slug>",public_profile_view,name='public'),
    
]
