
"""Global cart count"""
from .models import CartItem, Cart


def cart_count_processor(request):
    """Context processor to get the number of cart items"""
    cart_count = 0

    if request.user.is_authenticated:
        cart_obj = Cart.objects.filter(user=request.user).first()
        if cart_obj:
            cart_count = CartItem.objects.filter(cart=cart_obj).count()
    else:
        session_cart = request.session.get("cart", {})
        cart_count = len(session_cart)

    return {"cart_count": cart_count}
