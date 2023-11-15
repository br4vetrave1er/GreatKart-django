from django.shortcuts import render
from products.models import Products, ReviewandRating

def home(request):
    products = Products.objects.all().filter(is_available=True).order_by("-date_created")

    for product in products:
        reviews = ReviewandRating.objects.filter(product_id=product.id, status=True)

    product_count = products.count()
    context = {
        'products': products,
        'product_count': product_count,
    }

    return render(request, 'index.html', context)




