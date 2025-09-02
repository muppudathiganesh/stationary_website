from django.contrib import admin
from .models import Category, Product, Order, OrderItem

# --- Category ---
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ("name", "slug")


# --- Product ---
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "category", "price", "mrp", "featured", "trending", "back_to_school")
    list_filter = ("category", "featured", "trending", "back_to_school")
    search_fields = ("title", "sku")


# --- Order + OrderItem ---
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "status", "created", "updated", "get_total_cost"]
    list_filter = ["status", "created"]
    search_fields = ["user__username", "id"]
    inlines = [OrderItemInline]

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ["order", "product", "quantity", "price", "get_total_price"]
