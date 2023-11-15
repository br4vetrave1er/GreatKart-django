import datetime

from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from carts.models import CartItem
from .forms import OrderForm
from .models import Order, Payment, OrderProduct
import json
from products.models import Products
# Create your views here.
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage, send_mail
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from GreatKart import settings


def payments(request):
    try:
        body = json.loads(request.body)
        order = Order.objects.get(user=request.user, is_ordered=False, order_number=body["orderID"])
        # Transaction Details
        payment = Payment(
            user=request.user,
            payment_id=body["transID"],
            payment_method=body["payment_method"],
            amount_paid=order.order_total,
            status=body["status"],
        )
        payment.save()
        order.payment = payment
        order.is_ordered = True
        order.save()

        # mOVE CART ITEMS TO order product table
        cart_items = CartItem.objects.filter(user=request.user)

        for item in cart_items:
            orderproduct = OrderProduct()
            orderproduct.order_id = order.id
            orderproduct.payment = payment
            orderproduct.user_id = request.user.id
            orderproduct.product_id = item.product_id
            orderproduct.quantity = item.quantity
            orderproduct.product_price = item.product.price
            orderproduct.ordered = True
            orderproduct.save()

            cart_item = CartItem.objects.get(id=item.id)
            product_variation = cart_item.variations.all()
            orderproduct = OrderProduct.objects.get(id=orderproduct.id)
            orderproduct.variation.set(product_variation)
            orderproduct.save()

            # Reduce quantity of sold products
            print(item.id)
            product = Products.objects.get(id=item.product_id)
            product.stock -= item.quantity
            product.save()

        # remove product from cart
        CartItem.objects.filter(user=request.user).delete()

        user = request.user
        email = user.email
        mail_subject = 'Thank YOu for your order'
        message = render_to_string('orders/order_received_mail.html', {
            'user': user,
            'order': order
        })
        to_email = email
        email_from = settings.EMAIL_HOST_USER
        # send_email = EmailMessage(mail_subject, message, to=[to_email])
        send_mail(mail_subject, message, email_from, [to_email])

        data = {
            'order_number': order.order_number,
            'transID': payment.payment_id,
        }

        return JsonResponse(data)
    except:
        return HttpResponse("Please login to use this url")


def place_order(request, total=0, quantity=0):
    current_user = request.user

    cart_items = CartItem.objects.filter(user=current_user)
    if cart_items.count() <= 0:
        return redirect('store')

    grand_total = 0
    tax = 0
    for item in cart_items:
        total += (item.product.price * item.quantity)
        quantity += item.quantity
    tax = round((2 * total) / 100, 2)
    grand_total = round(total + tax, 2)

    if request.method == "POST":
        print("from post request")
        form = OrderForm(request.POST)
        if form.is_valid():
            data = Order()
            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.address_line_2 = form.cleaned_data['address_line_2']
            data.state = form.cleaned_data['state']
            data.city = form.cleaned_data['city']
            data.pincode = form.cleaned_data['pincode']
            data.phone_number = form.cleaned_data['phone_number']
            data.order_note = form.cleaned_data['order_note']
            data.tax = tax
            data.order_total = grand_total
            data.ip = request.META.get("REMOTE_ADDR")
            data.save()
            # Generate Order Number
            yr = int(datetime.date.today().strftime("%Y"))
            dt = int(datetime.date.today().strftime("%d"))
            mt = int(datetime.date.today().strftime("%m"))
            d = datetime.date(yr, mt, dt)
            current_date = d.strftime("%Y%m%d")
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()

            order = Order.objects.get(user=current_user, is_ordered=False, order_number=order_number, )
            context = {
                'order': order,
                'cart_items': cart_items,
                'total': total,
                'tax': tax,
                'grand_total': grand_total
            }
            return render(request, 'orders/payments.html', context)
        else:
            return redirect('checkout')


def order_placed(request):
    order_number = request.GET.get('order_number')
    transID = request.GET.get('payment_id')

    try:
        order = Order.objects.get(order_number=order_number, is_ordered=True)
        order_product = OrderProduct.objects.filter(order_id=order.id)
        payment = Payment.objects.get(payment_id=transID)
        subtotal = 0
        for i in order_product:
            subtotal += i.product_price * i.quantity

        context = {
            "order": order,
            "order_product": order_product,
            "payment_id": payment.payment_id,
            "subtotal": subtotal,
        }
        return render(request, "orders/order_placed.html", context)
    except (Payment.DoesNotExist, Order.DoesNotExist):
        return redirect('home')
