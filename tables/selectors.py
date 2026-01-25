from django.db.models import Exists, OuterRef

from orders.models import Order

from .models import Table

FINAL_STATUSES = ['PAID', 'CANCELLED']

def get_tables():
    return Table.objects.all()

def get_active_tables():
    return Table.objects.all(is_active=True)

def get_available_tables():
    
    active_orders = Order.objects.filter(
        table=OuterRef('pk')
    ).exclude(
        status__in=FINAL_STATUSES
    )

    return Table.objects.filter(
        is_active=True
    ).exclude(
        Exists(active_orders)
    )
