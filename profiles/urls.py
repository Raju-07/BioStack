from django.urls import path
from .views import (
    profile_list,
    profile_create,
    set_active_profile,
    theme_store,
    section_list_create,
    public_profile_view,
    delete_profile,
    delete_section,
    reorder_sections,
    update_theme,
    track_link_click
)

app_name = "profiles"

urlpatterns = [
    path("me/", profile_list, name="list"),
    path("create/", profile_create, name="create"),
    path("set-active/<int:profile_id>/", set_active_profile, name="set_active"),
    path("me/themes/", theme_store, name="themes"),
    path("me/sections/", section_list_create, name="sections"),
    # path("<slug:slug>/", public_profile_view, name="public"),
    path("<str:username>/<slug:profile_slug>/", public_profile_view, name="public"),
    path("me/sections/reorder/",reorder_sections, name="reorder_sections"),
    path("delete/<int:profile_id>",delete_profile,name='delete'),
    path("me/sections/delete/<int:section_id>/",delete_section, name="delete_section"),

    path('me/theme/update/',update_theme,name='update_theme'),
    #Tracking link click 
    path('track/click/<int:section_id>',track_link_click,name='track_click'),
]
