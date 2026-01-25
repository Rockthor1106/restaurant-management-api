from django.db import models

from accounts.models import User

class Table(models.Model):

    number = models.IntegerField(unique=True)
    capacity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(
        User,
        related_name='modified_tables',
        on_delete=models.SET_NULL,
        default=None,
        null=True
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Defines it avaible to be used'
    )

    @property
    def has_active_order(self):
        return self.orders.exclude(
            status__in = ['PAID', 'CANCELLED']
        ).exists()


