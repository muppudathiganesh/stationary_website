# shop/models.py
from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(
        Category,
        related_name="products",
        on_delete=models.CASCADE,
        null=True,  # allow null for safe migration
        blank=True,
    )
    title = models.CharField(max_length=150, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Selling price", blank=True, null=True)
    mrp = models.DecimalField(max_digits=10, decimal_places=2, help_text="Original price", null=True, blank=True)
    discount_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=4.5, blank=True, null=True)
    image = models.ImageField(upload_to="products/")
    sku = models.CharField(max_length=64, blank=True)
    featured = models.BooleanField(default=False, help_text='Show in "Featured Product"')
    trending = models.BooleanField(default=False, help_text='Show in "Trending"')
    back_to_school = models.BooleanField(default=False, help_text='Show in "Back to School"')
    bulk_offer_text = models.CharField(max_length=120, blank=True, help_text='e.g., "Buy 3 or more @ Rs. 101.20"')

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return self.title or f"Product #{self.pk}"


# shop/models.py
class Order(models.Model):
    STATUS_CHOICES = [
        ("Placed", "Placed"),
        ("Packed", "Packed"),
        ("Shipped", "Shipped"),
        ("Delivered", "Delivered"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Placed")

    # New fields - make them optional
    fullname = models.CharField(max_length=200, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    postal = models.CharField(max_length=20, blank=True, null=True)
    payment_method = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"

    def get_total_cost(self):
        return sum(item.get_total_price() for item in self.items.all())



class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.title} ({self.quantity})"

    def get_total_price(self):
        return self.price * self.quantity

