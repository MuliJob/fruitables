"""
  Web view functions
"""
from django.shortcuts import render

def home_page(request):
    """Home page function"""
    return render(request, 'index.html')
