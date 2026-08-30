from django.contrib import admin

from .models import Product, ProductVariant


class ProductVariantInline(admin.TabularInline):

    model = ProductVariant

    extra = 3

    fields = (
        "pack_size",
        "price",
        "stock_quantity",
        "availability",
    )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "category",
        "availability",
        "created_at",
    )

    search_fields = (
        "name",
        "category",
    )

    list_filter = (
        "category",
        "availability",
    )

    inlines = [
        ProductVariantInline
    ]


@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):

    list_display = (
        "product",
        "pack_size",
        "price",
        "stock_quantity",
        "availability",
    )

    list_filter = (
        "availability",
        "pack_size",
    )

    search_fields = (
        "product__name",
        "pack_size",
    )