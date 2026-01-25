from rest_framework.exceptions import ValidationError

from .models import Table

from accounts.models import User

def activate_table(table: Table, user: User):

    if table.is_active:
        raise ValidationError(f'Table is already activated')

    table.is_active = True
    table.modified_by = user
    table.save()

def deactivate_table(table: Table, user: User):

    if not table.is_active:
        raise ValidationError(f'Table is already deactivated')

    if table.has_active_order:
        raise ValidationError(f'Cannot deactivate a table with active orders')

    table.is_active = False
    table.modified_by = user
    table.save()




    
