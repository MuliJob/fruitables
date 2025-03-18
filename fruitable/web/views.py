"""
  Web view functions
"""
from django.shortcuts import render

from .models import Product



def home_page(request):
    """Home page function"""
    title = 'FRUITABLES - HOME'

    all_organics = Product.objects.all()
    vegetables = Product.objects.filter(product_category='Vegetables').all()
    fruits = Product.objects.exclude(product_category='Vegetables').all()

    context = {
        "title": title,
        "all_organics": all_organics,
        "vegetables": vegetables,
        "fruits": fruits,
    }

    return render(request, 'index.html', context)


def shop_page(request):
    """Shop page function"""
    title = 'FRUITABLES - SHOP'

    context = {
        "title": title
    }

    return render(request, 'shop.html', context)


def product_detail_page(request, pk):
    """Product detail page function"""
    title = 'FRUITABLES - PRODUCT DETAILS'

    product_detail = Product.objects.get(pk=pk)

    context = {
        "title": title,
        'product_detail': product_detail,
    }

    return render(request, 'shop-detail.html', context)


def cart_page(request):
    """Product cart page function"""
    title = 'FRUITABLES - CART'

    context = {
        "title": title
    }

    return render(request, 'cart.html', context)


def checkout_page(request):
    """Product checkout page function"""
    title = 'FRUITABLES - CHECKOUT'

    context = {
        "title": title
    }

    return render(request, 'checkout.html', context)


def testimonial_page(request):
    """Testimonials page function"""
    title = 'FRUITABLES - TESTIMONIALS'

    context = {
        "title": title
    }

    return render(request, 'testimonial.html', context)


def contact_page(request):
    """Contact page function"""
    title = 'FRUITABLES - CONTACT'

    context = {
        "title": title
    }

    return render(request, 'contact.html', context)
