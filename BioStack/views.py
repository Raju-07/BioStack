from django.shortcuts import render

def homepage(request):
    return render(request,'home.html')

def pricing(request):
    return render(request,'navbar/pricing.html')

def about_view(request):
    return render(request,'navbar/about.html')

def features_view(request):
    return render(request,'navbar/features.html')

def test(request):
    return render(request,'test.html')