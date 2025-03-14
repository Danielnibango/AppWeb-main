from django.shortcuts import render

# Create your views here.

def home(request):

    return render(request, "dashboard.html")

def dash(request):
    return render(request, 'dashboard.html')

 
