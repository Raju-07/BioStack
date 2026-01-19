from django.urls import path
from django.contrib.auth import views as auth_views
from .views import signup_view, login_view, logout_view,user_details

app_name = "accounts"

urlpatterns = [
    path("signup/", signup_view, name="signup"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("userdetails/",user_details,name='settings'),
]
