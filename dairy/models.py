from django.db import models


class Product(models.Model):

    name = models.CharField(max_length=200)

    description = models.TextField()

    category = models.CharField(max_length=100)

    image = models.ImageField(
        upload_to="products/",
        blank=True,
        null=True
    )

    availability = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class ProductVariant(models.Model):

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="variants"
    )

    pack_size = models.CharField(
        max_length=50
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    stock_quantity = models.PositiveIntegerField(
        default=0
    )

    availability = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"{self.product.name} - {self.pack_size}"