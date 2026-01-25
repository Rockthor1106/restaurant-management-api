from rest_framework.exceptions import ValidationError

from accounts.models import User

from .models import Product

def activate_product(product: Product, user: User):
    
    if product.is_active:
        raise ValidationError('Product is already activated')

    product.is_active = True
    product.modified_by = user
    product.save()

def deactivate_product(product: Product, user: User):

    if not product.is_active:
        raise ValidationError('Product is already deactivated')

    product.is_active = False
    product.modified_by = user
    product.save()
