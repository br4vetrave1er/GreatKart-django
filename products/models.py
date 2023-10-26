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


class VariationManager(models.Manager):
    def color(self):
        return super(VariationManager, self).filter(variation_category='color', is_active=True)

    def size(self):
        return super(VariationManager, self).filter(variation_category='size', is_active=True)


variation_category_choice = (
    ('color', 'color'),
    ('size', 'size'),
)


class Variations(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    variation_category = models.CharField(max_length=50, choices=variation_category_choice)
    variation_value = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now=True)

    objects = VariationManager()

    def __str__(self):
        return self.variation_value
