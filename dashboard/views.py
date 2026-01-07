from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required

@login_required
def dashboard_view(request):
    return render(request,'dashboard/index.html')
    

# Create your views here.
