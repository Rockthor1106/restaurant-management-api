from django.db import models

from accounts.models import User

class Product(models.Model):

    name = models.CharField(max_length=100, unique=True)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=3
    )
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(
        User, 
        related_name='products_created_by_user', 
        on_delete=models.SET_NULL, 
        blank=True, 
        null=True
    )
    modified_by = models.ForeignKey(
        User,
        related_name='modified_products',
        on_delete=models.SET_NULL,
        default=None,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def ___str___(self):
        return f'{self.name} (${self.price})'



