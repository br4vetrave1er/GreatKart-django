from django.contrib import admin
from .models import Products, Variations, ReviewandRating, ProductGallery
import admin_thumbnails

# Register your models here.


@admin_thumbnails.thumbnail('image')
class ProductGalleryInline(admin.TabularInline):
    model = ProductGallery
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'category', 'modified_date', 'is_available')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductGalleryInline]


class VariationsAdmin(admin.ModelAdmin):
    list_display = ('product', 'variation_category', 'variation_value', 'is_active')
    list_editable = ('is_active',)
    list_filter = ('product', 'variation_category')


admin.site.register(Products, ProductAdmin)
admin.site.register(Variations, VariationsAdmin)
admin.site.register(ReviewandRating)
admin.site.register(ProductGallery)
