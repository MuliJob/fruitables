"""
  Web view functions
"""
from django.shortcuts import render
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect


from .models import Cart, CartItem, Product


def home_page(request):
    """Home page function"""
    title = 'FRUITABLES - HOME'

    all_organics = Product.objects.all().order_by('-created_at')
    vegetables = Product.objects.filter(product_category='Vegetable').all().order_by('-created_at')
    fruits = Product.objects.exclude(product_category='Vegetable').all().order_by('-created_at')

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

    all_products = Product.objects.all().order_by('-created_at')

    context = {
        "title": title,
        "all_products": all_products,
    }

    return render(request, 'shop.html', context)


def product_detail_page(request, pk):
    """Product detail page function"""
    title = 'FRUITABLES - PRODUCT DETAILS'

    product_detail = Product.objects.get(pk=pk)
    related_products = Product.objects.exclude(
        id=product_detail.id).filter(
            product_category=product_detail.product_category).order_by('-created_at')
    categories = Product.objects.values(
        'product_category').annotate(count=Count('product_category'))

    context = {
        "title": title,
        'product_detail': product_detail,
        'related_products': related_products,
        'categories': categories,
    }

    return render(request, 'shop-detail.html', context)


def cart_page(request):
    """Product cart page function"""
    title = 'FRUITABLES - CART'

    context = {
        "title": title
    }

    return render(request, 'cart.html', context)


def cart_add(request, pk, qty=1):
    """Adding item to cart"""
    item = get_object_or_404(Product, pk=pk)

    if request.user.is_authenticated:
        # Logged-in user: Use database cart
        cart_obj, created = Cart.objects.get_or_create(
            user=request.user, defaults={"total": 0, "quantity": 0})

        # Check if the item is already in the cart
        cart_item, item_created = CartItem.objects.get_or_create(
            cart=cart_obj,
            product=item,
            defaults={"product_quantity": qty}
        )

        if not item_created:
            cart_item.product_quantity += qty
            cart_item.save()

        print("Item added to user cart")

    else:
        # Guest user: Use session-based cart
        cart = request.session.get("cart", {})

        if str(pk) in cart:
            cart[str(pk)]["quantity"] += qty
        else:
            cart[str(pk)] = {
                "product_name": item.product_name,
                "product_price": item.product_price,
                "quantity": qty
            }

        request.session["cart"] = cart  # Save cart to session
        request.session.modified = True

        print("Item added to session cart")

    return JsonResponse({"message": "Item added to cart successfully"})


def transfer_session_cart(request):
    """Transfer session cart items to user cart after login"""
    if request.user.is_authenticated and "cart" in request.session:
        cart_obj, created = Cart.objects.get_or_create(
            user=request.user, defaults={"total": 0, "quantity": 0})

        for pk, item in request.session["cart"].items():
            product = Product.objects.get(pk=pk)
            cart_item, item_created = CartItem.objects.get_or_create(
                cart=cart_obj,
                product=product,
                defaults={"product_quantity": item["quantity"]}
            )

            if not item_created:
                cart_item.product_quantity += item["quantity"]
                cart_item.save()

        del request.session["cart"]  # Clear session cart
        request.session.modified = True


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
