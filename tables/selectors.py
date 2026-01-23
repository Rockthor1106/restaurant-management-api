from .models import Table

def get_tables():
    return Table.objects.all()