"""
URL configuration for fruitable project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name="home"),
    path('shop', views.shop_page, name="shop"),
    path('product-details/<uuid:pk>', views.product_detail_page, name="product_detail"),
    path('cart', views.cart_page, name="cart"),
    path('cart-add/<uuid:pk>', views.cart_add, name="cart_add"),
    path('checkout', views.checkout_page, name="checkout"),
    path('testimonial', views.testimonial_page, name="testimonial"),
    path('contact', views.contact_page, name="contact"),
]
