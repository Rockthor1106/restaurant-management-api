from .models import Product

def get_products():
    return Product.objects.all()

def get_active_products():
    return Product.objects.filter(is_active=True)