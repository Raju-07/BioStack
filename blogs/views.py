from django.shortcuts import render
from .models import Blogs

# Create your views here.
def blog_view(request):
    return render(request,'pages/blog.html')