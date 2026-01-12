from django.urls import path
from .views import (
    profile_list,
    profile_create,
    section_list_create,
    public_profile_view,
)

app_name = "profiles"

urlpatterns = [
    path("me/", profile_list, name="list"),
    path("create/", profile_create, name="create"),
    path("me/<int:profile_id>/sections/", section_list_create, name="sections"),
    path("<slug:slug>/", public_profile_view, name="public"),
]
