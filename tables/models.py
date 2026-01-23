from django.db import models

class Table(models.Model):

    number = models.IntegerField()
    capacity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateField(auto_now=True)
    is_active = models.BooleanField(
        default=True,
        verbose_name='Defines it avaible to be used'
    )
