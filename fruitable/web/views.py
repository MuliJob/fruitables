"""
  Web view functions
"""
from decimal import Decimal
from django.contrib.postgres.search import SearchVector
from django.shortcuts import render
from django.urls import reverse
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator


from .models import Cart, CartItem, Product, Review
from .forms import ReviewForm



def search(request):
    """Search function"""
    title = 'FRUITABLES - SEARCH'
    search_result = Product.objects.annotate(
        search=SearchVector("product_name", "product_origin",
                            "product_price", "product_check",
                            "product_category", "product_description",
                            "product_detail_description"),)
    paginator = Paginator(search_result, 8)
    page_number = request.GET.get("search")
    all_search_obj = paginator.get_page(page_number)

    context = {
        "title": title,
        "all_search_obj": all_search_obj,
    }

    return render(request, "search.html", context)



def home_page(request):
    """Home page function"""
    title = 'FRUITABLES - HOME'

    all_organics = Product.objects.all().order_by('-created_at')
    paginator = Paginator(all_organics, 8)
    page_number = request.GET.get("home")
    all_page_obj = paginator.get_page(page_number)

    vegetables = Product.objects.filter(product_category='Vegetable').all().order_by('-created_at')
    fruits = Product.objects.exclude(product_category='Vegetable').all().order_by('-created_at')

    context = {
        "title": title,
        "all_page_obj": all_page_obj,
        "vegetables": vegetables,
        "fruits": fruits,
    }

    return render(request, 'index.html', context)


def shop_page(request):
    """Shop page function"""
    title = 'FRUITABLES - SHOP'

    all_products = Product.objects.all().order_by('-created_at')
    paginator = Paginator(all_products, 9)
    page_number = request.GET.get("shop")
    page_obj = paginator.get_page(page_number)

    categories = Product.objects.values(
        'product_category').annotate(count=Count('product_category'))

    vegetables = Product.objects.exclude(
        product_category='Fruits').all().order_by('-created_at')[:3]

    context = {
        "title": title,
        "page_obj": page_obj,
        'categories': categories,
        "vegetables": vegetables,
    }

    return render(request, 'shop.html', context)


def product_detail_page(request, pk):
    """Product detail page function"""
    title = 'FRUITABLES - PRODUCT DETAILS'

    product_detail = get_object_or_404(Product, pk=pk)
    related_products = Product.objects.exclude(
        id=product_detail.id).filter(
            product_category=product_detail.product_category).order_by('-created_at')
    categories = Product.objects.values(
        'product_category').annotate(count=Count('product_category'))
    fruits = Product.objects.exclude(product_category='Vegetable').all().order_by('-created_at')[:4]
    reviews = Review.objects.filter(product=pk).order_by('-created_at')

    average_rating = product_detail.get_average_rating()

    print(f"Average Rating for Product {product_detail.id}: {average_rating}")

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = get_object_or_404(Product, id=pk)
            review.star = request.POST.get('star', 1)
            review.save()
            messages.success(request, "Review posted successful")

            return redirect("product_detail", pk=pk)
        else:
            print("Form Errors:", form.errors)
            messages.error(request,
                           "Something happened when posting your review. Please try again!")
    else:
        form = ReviewForm()

    context = {
        "title": title,
        'product_detail': product_detail,
        'related_products': related_products,
        'categories': categories,
        'fruits': fruits,
        "form": form,
        "reviews": reviews,
        "average_rating": average_rating,
    }

    return render(request, 'shop-detail.html', context)


def cart_page(request):
    """Product cart page function"""
    title = "FRUITABLES - CART"
    cart_items = []
    total_price = 0
    total_shipping_fee = 0

    if request.user.is_authenticated:
        cart_obj = Cart.objects.filter(user=request.user).first()
        if cart_obj:
            cart_items = CartItem.objects.filter(cart=cart_obj)
            total_price = sum(item.total_price for item in cart_items)
            total_shipping_fee = sum(item.shipping_fee for item in cart_items)
    else:
        session_cart = request.session.get("cart", {})
        for pk, item in session_cart.items():
            product = get_object_or_404(Product, pk=pk)
            shipping_fee = product.shipping_fee if hasattr(product, "shipping_fee") else 0

            cart_items.append({
                "product": product,
                "product_quantity": item["quantity"],
                "total_price": product.product_price * item["quantity"],
                "shipping_fee": shipping_fee,
            })
            total_price += product.product_price * item["quantity"]
            total_shipping_fee += shipping_fee

    grand_total = total_price + total_shipping_fee

    context = {
        "title": title,
        "cart_items": cart_items,
        "total_price": total_price,
        "total_shipping_fee": total_shipping_fee,
        "grand_total": grand_total,
    }

    return render(request, "cart.html", context)


def cart_add(request, pk, qty=1):
    """Adding item to cart without increasing quantity if already exists"""
    item = get_object_or_404(Product, pk=pk)

    if request.user.is_authenticated:
        cart_obj, created = Cart.objects.get_or_create(
            user=request.user, defaults={"total": Decimal(0), "quantity": 0})

        # Check if the product already exists in the cart
        cart_item = CartItem.objects.filter(cart=cart_obj, product=item).first()

        if cart_item:
            messages.warning(request, "Item is already in your cart.")
        else:
            CartItem.objects.create(cart=cart_obj, product=item, product_quantity=qty)
            messages.success(request, "Item added to cart.")

    else:
        cart = request.session.get("cart", {})

        if str(pk) in cart:
            messages.warning(request, "Item is already in your cart.")
        else:
            cart[str(pk)] = {
                "product_name": item.product_name,
                "product_price": float(item.product_price),
                "quantity": qty
            }
            request.session["cart"] = cart
            request.session.modified = True
            messages.success(request, "Item added to cart.")

    return redirect(reverse("cart_page"))


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

        del request.session["cart"]
        request.session.modified = True

def cart_update(request, pk, action):
    """Increase or decrease cart item quantity."""
    product = get_object_or_404(Product, pk=pk)

    if request.user.is_authenticated:
        cart_obj = Cart.objects.filter(user=request.user).first()
        if cart_obj:
            cart_item = CartItem.objects.filter(cart=cart_obj, product=product).first()
            if cart_item:
                if action == "increase":
                    cart_item.product_quantity += 1
                elif action == "decrease" and cart_item.product_quantity > 1:
                    cart_item.product_quantity -= 1
                cart_item.save()
    else:
        session_cart = request.session.get("cart", {})
        if str(pk) in session_cart:
            if action == "increase":
                session_cart[str(pk)]["quantity"] += 1
            elif action == "decrease" and session_cart[str(pk)]["quantity"] > 1:
                session_cart[str(pk)]["quantity"] -= 1
            request.session["cart"] = session_cart
            request.session.modified = True

    return redirect("cart_page")

def cart_remove(request, pk):
    """Remove an item from the cart."""
    if request.user.is_authenticated:
        cart_obj = Cart.objects.filter(user=request.user).first()
        if cart_obj:
            CartItem.objects.filter(cart=cart_obj, product_id=pk).delete()
            messages.success(request, "Item removed from cart.")
    else:
        session_cart = request.session.get("cart", {})
        if str(pk) in session_cart:
            del session_cart[str(pk)]
            request.session["cart"] = session_cart
            request.session.modified = True
            messages.success(request, "Item removed from cart.")

    return redirect("cart_page")


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
