"""
URL configuration for BioStack project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from BioStack import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path('',views.homepage,name='home'),
    path('test/',views.test),
    path('pricing/',views.pricing,name='pricing'),
    path('support/',views.support,name='support'),
    path('features/',views.features_view,name='features'),
    path('about-us/',views.about_view,name='about'),

    #Footer Views
    path('blog/',views.blog_view,name='blog'),
    path('showcase/',views.showcase_view,name='showcase'),
    path('terms/',views.terms_view,name='terms'),
    path('templates/',views.templates_view,name='templates'),
    path('templates/preview/<int:theme_id>/', views.theme_preview_view, name='theme_preview'),
    path('privacy/',views.privacy_view,name='privacy'),
    path('careers/',views.career_view,name='careers'),

 # Namespaced apps
    path("auth/", include(("accounts.urls", "accounts"), namespace="accounts")),
    path("dashboard/", include(("dashboard.urls", "dashboard"), namespace="dashboard")),

    # PASSWORD RESET 
    path("password-reset/", auth_views.PasswordResetView.as_view(template_name="accounts/password_reset.html",),name="password_reset", ),
    path("password-reset/done/",auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_reset_done.html" ),name="password_reset_done",),
    path( "reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_confirm.html"),name="password_reset_confirm", ),
    path("reset/done/",auth_views.PasswordResetCompleteView.as_view(template_name="accounts/password_reset_complete.html"),name="password_reset_complete", ),
    #Profile 
    path("profile/", include(("profiles.urls", "profiles"), namespace="profiles")),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)