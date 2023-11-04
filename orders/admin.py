from django.contrib import admin
from .models import Payment, OrderProduct, Order

# Register your models here.

class OrderProductAdmin(admin.ModelAdmin):
    model = OrderProduct
    readonly_fields = ('payment', 'user', 'product', 'ordered')

class OrderAdmin(admin.ModelAdmin):
    list_display = ["order_number", "full_name", "phone_number", "order_total", "is_ordered", "status"]
    list_filter = ["status", "is_ordered"]
    search_fields = ["order_number", "first_name", "last_name", "status"]
    list_per_page = 20

admin.site.register(Payment)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderProduct, OrderProductAdmin)
