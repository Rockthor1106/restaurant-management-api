from django.contrib.auth import get_user_model

from orders.models import Order

from products.models import Product

from .models import OrderItem

User = get_user_model()


def get_order_items():
    return OrderItem.objects.all()

def get_order_items_by_user(user: User):
    return OrderItem.objects.filter(order__created_by=user)

def get_items_of_order(order: Order):
    return OrderItem.objects.filter(order=order)

def get_order_item(order: Order, product: Product):
    return OrderItem.objects.filter(
        order=order,
        product=product
    ).first()
