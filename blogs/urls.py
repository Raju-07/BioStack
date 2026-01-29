from django.urls import path
from blogs import views

urlpatterns = [
    path("",views.blog_view,name='blog')
]
