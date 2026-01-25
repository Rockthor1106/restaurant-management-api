from rest_framework.exceptions import ValidationError

from .models import Order, OrderStatus

from tables.models import Table

from .selectors import get_active_orders_of_table


def create_order(table: Table, user):
    
    has_active_order = get_active_orders_of_table(table).exists()

    if has_active_order:
        raise ValidationError('This table has an active order')

    if not table.is_active:
        raise ValidationError('This table is not active')

    return Order.objects.create(
        table=table,
        created_by=user,
    )   

def change_status(order: Order, new_status):
    order.change_status(new_status)

def start_preparation(order: Order):
    if not order.is_active:
        raise ValidationError('Cannot start preparation. The order is already closed.')
    
    order.change_status(OrderStatus.IN_PREPARATION)

def mark_ready(order: Order):
    if not order.is_active:
        raise ValidationError(f'Cannot mark as ready. The order is already closed.')
    
    order.change_status(OrderStatus.READY)

def deliver(order: Order):
    if not order.is_active:
        raise ValidationError(f'Cannot deliver. The order is already closed.')
    
    order.change_status(OrderStatus.DELIVERED)

def pay_order(order: Order):
    if not order.is_active:
        raise ValidationError('Order is already closed')
    
    if order.status != OrderStatus.DELIVERED:
        raise ValidationError('Only delivered orders can be paid')

    order.change_status(OrderStatus.PAID)

def cancel_order(order: Order):
    if not order.is_active:
        raise ValidationError('Order is already closed')

    if order.status != OrderStatus.CREATED:
        raise ValidationError(
            'Only orders that have not started preparation can be cancelled'
        )

    order.change_status(OrderStatus.CANCELLED)