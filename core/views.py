from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .models import Category, Product, Order, OrderItem
from core.cart import Cart

    # ---------------- HOME / SHOP / ABOUT ---------------- #

def home(request):
        context = {
            "featured": Product.objects.filter(featured=True)[:8],
            "trending": Product.objects.filter(trending=True)[:8],
            "back_to_school": Product.objects.filter(back_to_school=True)[:8],
        }
        return render(request, "core/home.html", context)

def aboutus(request):
        return render(request, "core/aboutus.html")

def contact(request):
        return render(request, "core/contact.html")

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

def signin(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            next_url = request.GET.get("next") or "billing_detail"
            return redirect(next_url)
        else:
            return render(request, "core/signin.html", {"error": "Invalid credentials"})

    
    return render(request, "core/signin.html")



def shop(request, slug=None):
        category = None
        categories = Category.objects.all()
        products = Product.objects.all()

        # Category filter
        if slug:
            category = get_object_or_404(Category, slug=slug)
            products = products.filter(category=category)

        # Search filter
        query = request.GET.get("q")
        if query:
            products = products.filter(title__icontains=query)

        # Pagination
        paginator = Paginator(products, 9)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        return render(request, "core/shop.html", {
            "categories": categories,
            "products": page_obj,
            "category": category,
            "query": query,
        })
# ---------------- PRODUCT DETAIL ---------------- #

from django.shortcuts import render, get_object_or_404
from .models import Product

def product_detail(request, slug):
    """Single product detail page"""
    product = get_object_or_404(Product, slug=slug)

    # Related products from the same category (exclude current)
    related_products = Product.objects.filter(
        category=product.category
    ).exclude(id=product.id)[:4]

    return render(request, "core/product_detail.html", {
        "product": product,
        "related_products": related_products,
    })
from django.shortcuts import get_object_or_404, redirect
from core.models import Product

from core.models import Product, Order, OrderItem
from core.cart import Cart


def buy_now(request, product_id):
    """Direct checkout for one product"""
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get("quantity", 1))

    cart = Cart(request)
    cart.clear()
    cart.add(product=product, quantity=quantity)

    return redirect("checkout")


    # ---------------- CART ---------------- #

def cart_detail(request):
        cart = Cart(request)
        total_price = sum(item['total_price'] for item in cart)
        return render(request, "core/cart_detail.html", {"cart": cart, "total_price": total_price})


def cart_update(request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)

        if request.method == "POST":
            quantity = int(request.POST.get("quantity", 1))

            if "increase" in request.POST:
                quantity += 1
            elif "decrease" in request.POST and quantity > 1:
                quantity -= 1

            # Use add() with override_quantity to "update"
            cart.add(product=product, quantity=quantity, override_quantity=True)

        return redirect("cart_detail")



def cart_remove(request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)

        if request.method == "POST":
            cart.remove(product)

        return redirect('cart_detail')


    # ---------------- BILLING / CHECKOUT ---------------- #

from django.contrib.auth.decorators import login_required

@login_required
def billing_detail(request):
    cart = Cart(request)
    total_price = sum(item['total_price'] for item in cart)
    return render(request, "core/billing_detail.html", {"cart": cart, "total_price": total_price})


from decimal import Decimal
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from .models import Order, OrderItem
from core.cart import Cart

@login_required
def checkout(request):
    cart = Cart(request)

    if request.method == "POST":
        fullname = request.POST.get("fullname")
        phone = request.POST.get("phone")
        address = request.POST.get("address")
        city = request.POST.get("city")
        postal = request.POST.get("postal")
        payment = request.POST.get("payment")

        with transaction.atomic():
            order = Order.objects.create(
                user=request.user,
                status="Placed",
                fullname=fullname,
                phone=phone,
                address=address,
                city=city,
                postal=postal,
                payment_method=payment,
            )

            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item["product"],
                    quantity=item["quantity"],
                    price=Decimal(item["price"]),  # convert to Decimal
                )

        cart.clear()
        return redirect("order_tracking", order_id=order.id)

    return redirect("cart_detail")



    # ---------------- ORDERS ---------------- #

@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by("-created")
    return render(request, "core/my_orders.html", {"orders": orders})


@login_required
def order_tracking(request, order_id):
    STATUS_FLOW = ["Placed", "Packed", "Shipped", "Delivered"]
    order = get_object_or_404(Order, id=order_id, user=request.user)

    current_index = STATUS_FLOW.index(order.status)
    progress = int(((current_index + 1) / len(STATUS_FLOW)) * 100)

    return render(request, "core/tracking.html", {
        "order": order,
        "status_flow": STATUS_FLOW,
        "current_index": current_index,
        "progress": progress,
    })
from datetime import timedelta
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Order

@login_required
def order_tracking(request, order_id):
    STATUS_FLOW = ["Placed", "Packed", "Shipped", "Delivered"]
    order = get_object_or_404(Order, id=order_id, user=request.user)

    current_index = STATUS_FLOW.index(order.status)
    progress = int(((current_index + 1) / len(STATUS_FLOW)) * 100)

    # Dynamic delivery estimate
    if order.status == "Placed":
        delivery_estimate = order.created + timedelta(days=5)
    elif order.status == "Packed":
        delivery_estimate = order.created + timedelta(days=4)
    elif order.status == "Shipped":
        delivery_estimate = order.created + timedelta(days=2)
    elif order.status == "Delivered":
        delivery_estimate = order.updated  # actual delivery date
    else:
        delivery_estimate = None

    return render(request, "core/tracking.html", {
        "order": order,
        "status_flow": STATUS_FLOW,
        "current_index": current_index,
        "progress": progress,
        "delivery_estimate": delivery_estimate,
    })
# shop/views.py
from django.shortcuts import render
from .models import Product

def search_view(request):
    query = request.GET.get('q', '')
    products = Product.objects.filter(title__icontains=query) if query else Product.objects.all()
    return render(request, 'search_results.html', {'products': products, 'query': query})


# from django.shortcuts import render
# from django.db.models import Q
# from .models import Product, Category   # import your models

# def product_list(request, category_slug=None):
#     products = Product.objects.all()
#     categories = Category.objects.all()
#     category = None

#     # Filter by category
#     if category_slug:
#         category = Category.objects.get(slug=category_slug)
#         products = products.filter(category=category)

#     # Filter by price ranges
#     selected_prices = request.GET.getlist("price")
#     if selected_prices:
#         price_filter = Q()
#         for price_range in selected_prices:
#             low, high = map(int, price_range.split("-"))
#             price_filter |= Q(price__gte=low, price__lte=high)
#         products = products.filter(price_filter)

#     return render(request, "shop/product_list.html", {
#         "products": products,
#         "categories": categories,
#         "category": category,
#         "selected_prices": selected_prices,   # 👈 pass to template
#     })
