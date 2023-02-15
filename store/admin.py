from django.contrib import admin

from store.models import Lessons, Product, Order


@admin.register(Lessons)
class LessonsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'access_level')
    fields = ('id', 'name', 'access_level', 'description', 'video_file')
    readonly_fields = ('id',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price')
    fields = ('id', 'name', 'price', 'description', 'stripe_product_price_id')
    readonly_fields = ('id',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'initiator', 'created', 'status', 'product')
    fields = ('id', 'initiator', 'created', 'status', 'product')
    readonly_fields = ('id', 'initiator', 'created', 'status', 'product')
