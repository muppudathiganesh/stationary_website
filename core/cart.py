# core/cart.py
from decimal import Decimal
from django.conf import settings
from .models import Product

class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, quantity=1, override_quantity=False):
        product_id = str(product.id)
        if product_id not in self.cart or isinstance(self.cart[product_id], int):
            # Store product info as dict
            self.cart[product_id] = {
                'quantity': 0,
                'price': str(product.price)
            }
        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity

        self.save()

    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def clear(self):
        self.session[settings.CART_SESSION_ID] = {}
        self.session.modified = True

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            item = self.cart[str(product.id)]
            # Convert old int entries to dict
            if isinstance(item, int):
                item = {'quantity': item, 'price': str(product.price)}
            else:
                item = item.copy()
            item['product'] = product
            item['total_price'] = Decimal(item['price']) * item['quantity']
            yield item

    def __len__(self):
        total_quantity = 0
        for item in self.cart.values():
            if isinstance(item, int):
                total_quantity += item
            else:
                total_quantity += item.get('quantity', 0)
        return total_quantity
