from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    
    path('', home),
    path('dashboard.htm', dash, name='dashboard'),
    
]