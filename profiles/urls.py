from django.urls import path
from .views import profile_view

app_name = "profiles"

urlpatterns = [
    path("me/", profile_view, name="me"),
]
