from django.shortcuts import render

def homepage(request):
    return render(request,'home.html')

def test(request):
    return render(request,'test.html')