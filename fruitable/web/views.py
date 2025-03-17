"""
  Web view functions
"""
from django.shortcuts import render

def home_page(request):
    """Home page function"""
    title = 'FRUITABLES - HOME'

    context = {
        "title": title
    }

    return render(request, 'index.html', context)


def shop_page(request):
    """Shop page function"""
    title = 'FRUITABLES - SHOP'

    context = {
        "title": title
    }

    return render(request, 'shop.html', context)
