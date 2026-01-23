from django.db import models

from django.core.exceptions import ValidationError

from tables.models import Table

from accounts.models import User


class OrderStatus(models.TextChoices):

    CREATED = 'CREATED', 'Created'
    IN_PREPARATION = 'IN_PREPARATION', 'In preparation'
    READY = 'READY', 'Ready'
    DELIVERED = 'DELIVERED', 'Delivered'
    PAID = 'PAID', 'Paid'
    CANCELLED = 'CANCELLED', 'Cancelled'


class Order(models.Model):

    table = models.ForeignKey(Table, related_name='orders', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=OrderStatus.choices, default=OrderStatus.CREATED)
    created_by = models.ForeignKey(User, related_name='orders_created_by_user', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    VALID_TRANSITIONS = {
        OrderStatus.CREATED: {OrderStatus.IN_PREPARATION, OrderStatus.CANCELLED},
        OrderStatus.IN_PREPARATION: {OrderStatus.READY},
        OrderStatus.READY: {OrderStatus.DELIVERED},
        OrderStatus.DELIVERED: {OrderStatus.PAID},
        OrderStatus.PAID: set(),
        OrderStatus.CANCELLED: set()
    }

    class Meta:
        ordering = ['-created_at']

    @property
    def is_active(self):
        return self.status not in [OrderStatus.PAID, OrderStatus.CANCELLED]

    def change_status(self, new_status):
        if new_status not in self.VALID_TRANSITIONS[self.status]:
            raise ValidationError(
                f'Cannot change status from {self.status} to {new_status}'
            )

        self.status = new_status
        self.save(update_fields=['status'])
    
