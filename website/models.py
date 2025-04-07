from django.db import models
from django.contrib.auth.models import User, Group


class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    starting_price = models.DecimalField(max_digits=10, decimal_places=2)
    reserve_price = models.DecimalField(max_digits=10, decimal_places=2)
    auction_end_time = models.DateTimeField()

    def __str__(self):
        return self.name

