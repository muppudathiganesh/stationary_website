"""
URL configuration for stationery_store project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

# Import views properly
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Core pages
    path('', views.home, name='home'),
    path('aboutus/', views.aboutus, name='aboutus'),
    path('contact/', views.contact, name='contact'),


    # Shop
    path("shop/", views.shop, name="shop"),
    path("shop/<slug:slug>/", views.shop, name="shop_by_category"),
    path("product/<slug:slug>/", views.product_detail, name="product_detail"),

    # Cart
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/update/<int:product_id>/', views.cart_update, name='cart_update'),
    path('cart/remove/<int:product_id>/', views.cart_remove, name='cart_remove'),

    # Billing & Checkout
    path("signin/", views.signin, name="signin"),
    path("billing/", views.billing_detail, name="billing_detail"),
    path("checkout/", views.checkout, name="checkout"),


    # Orders
    path("my-orders/", views.my_orders, name="my_orders"),
    path("tracking/<int:order_id>/", views.order_tracking, name="order_tracking"),

    path('search/', views.search_view, name='search'),
] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
