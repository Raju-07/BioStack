from django.urls import path
from .views import (
    profile_list,
    profile_create,
    set_active_profile,
    profile_dashboard,
    section_list_create,
    public_profile_view,
)

app_name = "profiles"

urlpatterns = [
    path("me/", profile_list, name="list"),
    path("create/", profile_create, name="create"),
    path("set-active/<int:profile_id>/", set_active_profile, name="set_active"),
    path("me/dashboard/", profile_dashboard, name="dashboard"),
    path("me/sections/", section_list_create, name="sections"),
    path("<slug:slug>/", public_profile_view, name="public"),
]
