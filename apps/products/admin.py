from django.contrib import admin
from unfold.admin import TabularInline
from django.utils.html import format_html

from .models import Product, ProductImage

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    readonly_fields = ('preview',)

    def preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="height: 50px;" />',
                obj.image.url
            )
        return "-"

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'seller',
        'price',
        'stock',
        'is_available',
        'created_at'
    )

    list_filter = (
        'is_available',
        'created_at',
        'category'
    )

    search_fields = (
        'name',
        'description'
    )

    prepopulated_fields = {'slug': ('name',)}

    inlines = [ProductImageInline]

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'is_main')