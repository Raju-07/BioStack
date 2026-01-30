from django.shortcuts import render,get_object_or_404
from .models import Blogs

# Create your views here.
def blog_view(request):
    blogs = Blogs.objects.all().order_by("-id")

    return render(request,'pages/blog.html',{"blogs":blogs})

def blog_details(request,slug):
    blog = get_object_or_404(Blogs, slug = slug)
    return render(request,"pages/blog_details.html",{"blog":blog})
