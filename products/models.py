from django.db import models
from category.models import Category
from django.urls import reverse


# Create your models here.


class Products(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    price = models.FloatField()
    description = models.TextField(max_length=200, blank=True)
    stock = models.IntegerField()
    image = models.ImageField(upload_to='photos/products', blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    is_available = models.BooleanField(default=True)

    # required
    date_created = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def get_url(self):
        return reverse('product_detail', args=[self.category.slug, self.slug])
    def __str__(self):
        return self.name
