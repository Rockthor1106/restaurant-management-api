from rest_framework.exceptions import ValidationError

from orders.models import Order

from products.models import Product

from .models import OrderItem

from .selectors import get_items_of_order, get_order_item


def create_order_item(order: Order, product: Product, quantity: int):

    if not order.is_active:
        raise ValidationError("Cannot assign items to an inactive order")

    if not product.is_active:
        raise ValidationError("Cannot add an inactive product to an order")

    found_item = get_order_item(order, product)

    if found_item:
        quantity += found_item.quantity
        found_item.quantity = quantity
        found_item.save()

        return found_item

    else: 
        return OrderItem.objects.create(
            order=order,
            product=product,
            product_name=product.name,
            unit_price=product.price,
            quantity=quantity
        )


def update_order_item_quantity(order_item: OrderItem, quantity: int):

    if not order_item.order.is_active:
        raise ValidationError("Cannot update an item of an inactive order")

    order_item.quantity = quantity
    order_item.save()

    return order_item

def delete_order_item(order_item: OrderItem):

    if not order_item.order.is_active:
        raise ValidationError("Cannot delete an item of an inactive order")

    order_item.delete()