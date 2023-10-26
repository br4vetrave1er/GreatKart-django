from django.shortcuts import render
from products.models import Products


def home(request):
    products = Products.objects.all().filter(is_available=True)
    product_count = products.count()
    context = {
        'products': products,
        'product_count': product_count,
    }

    return render(request, 'index.html', context)




