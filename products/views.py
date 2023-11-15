from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Products, ReviewandRating, ProductGallery
from category.models import Category
from .forms import ReviewForms

from carts.models import CartItem
from carts.views import cart_id
from django.core.paginator import EmptyPage, Paginator, PageNotAnInteger
from django.db.models import Q

from orders.models import OrderProduct


# Create your views here.


def store(request, category_slug=None):
    categories = None
    products = None
    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Products.objects.all().filter(category=categories, is_available=True)
        paginator = Paginator(products, 4)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()
    else:
        products = Products.objects.all().filter(is_available=True).order_by('id')
        paginator = Paginator(products, 6)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()
    context = {
        'products': paged_products,
        'product_count': product_count,

    }
    return render(request, 'store/store.html', context)


def product_detail(request, category_slug, product_slug):
    try:
        single_product = Products.objects.get(category__slug=category_slug, slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=cart_id(request), product=single_product).exists()

    except Exception as e:
        raise e
    if request.user.is_authenticated:
            try:
                order_product = OrderProduct.objects.filter(user=request.user, product_id=single_product.id).exists()
            except order_product.DoesNotExist:
                order_product = None
    else:
        order_product = None

    reviews = ReviewandRating.objects.filter(product_id=single_product.id, status=True)

    # Get the product gallery
    product_gallery = ProductGallery.objects.filter(product_id=single_product.id)

    context = {
        'single_product': single_product,
        'in_cart': in_cart,
        'order_product': order_product,
        'reviews': reviews,
        'product_gallery': product_gallery,
    }
    return render(request, 'store/product-detail.html', context)


def search(request):
    try:
        if 'keyword' in request.GET:
            keyword = request.GET['keyword']
            if keyword:
                products = Products.objects.order_by('-date_created').filter(
                    Q(description__icontains=keyword) | Q(name__icontains=keyword))
        product_count = products.count()
        context = {
            'products': products,
            'product_count': product_count,
        }
        return render(request, 'store/store.html', context)
    except:
        return HttpResponse("Please add argument to the search field to use this url")


def submit_review(request, product_id):
    url = request.META.get("HTTP_REFERER")
    if request.method == "POST":
        try:
            review = ReviewandRating.objects.get(user__id=request.user.id, product__id=product_id)
            form = ReviewForms(request.POST, instance=review)
            form.save()
            messages.success(request, "Your review has been updated")
            return redirect(url)
        except ReviewandRating.DoesNotExist:
            form = ReviewForms(request.POST)
            if form.is_valid():
                data = ReviewandRating()
                data.subject = form.cleaned_data['subject']
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.ip = request.META.get("REMOTE_ADDR")
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
                messages.success(request, "Your review has been updated")
                return redirect(url)


