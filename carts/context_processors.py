from .models import Cart, CartItem
from .views import cart_id


def counter(request):
    item_count = 0
    if 'admin' in request.path:
        return {}
    else:
        try:
            cart = Cart.objects.filter(cart_id=cart_id(request))
            if request.user.is_authenticated:
                cart_items = CartItem.objects.all().filter(user=request.user)
            else:
                cart_items = CartItem.objects.all().filter(cart=cart[:1])
            for item in cart_items:
                item_count += item.quantity
        except Cart.DoesNotExist:
            item_count = 0

    return dict(item_count=item_count)
