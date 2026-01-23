from .models import Order, OrderStatus

from tables.models import Table


def get_orders():
    return Order.objects.all()

def get_active_orders_of_table(table: Table):
    return Order.objects.filter(table=table).exclude(
        status__in = [OrderStatus.PAID, OrderStatus.CANCELLED]
    )