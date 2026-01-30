from django.db import models

from orders.models import Order
from products.models import Product


class OrderItem(models.Model):

    order = models.ForeignKey(Order, related_name='order_items', on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, 
        related_name='order_items',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    product_name = models.CharField(max_length=100)
    unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=3
    )
    quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['order', 'product'],
                name='unique_product_per_order'
            )
        ]

    @property
    def subtotal(self):
        return self.quantity * self.unit_price