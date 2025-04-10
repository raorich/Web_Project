from django.db import models
from django.contrib.auth.models import User, Group

# Our data base model
class Store(models.Model):
    name = models.CharField(max_length=255)
    users = models.ManyToManyField(User, related_name='stores')
    products = models.ManyToManyField('Product', related_name='stores')

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    subname = models.CharField(max_length=255)
    category = models.CharField(max_length=100) # art, automobiles, watch
    starting_price = models.DecimalField(max_digits=10, decimal_places=2)
    reserve_price = models.DecimalField(max_digits=10, decimal_places=2)
    auction_end_time = models.DateTimeField()

    def __str__(self):
        return self.name

class AcquisitionHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='acquisition_history')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.product.name} on {self.date}'

class Watch(Product):
    brand = models.CharField(max_length=100)
    documentation = models.CharField(max_length=255)
    case = models.CharField(max_length=255)
    model = models.CharField(max_length=100)
    condition = models.CharField(max_length=100)
    year = models.PositiveIntegerField()
    #Falta la gestion de las imagenes

class Art(Product):
    artist = models.CharField(max_length=100)
    year = models.IntegerField()

class Automobiles(Product):
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

class SalesHistory(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='sales_history')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.store.name} sold {self.product.name} on {self.date}'

class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bids')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='bids')
    bid_amount = models.DecimalField(max_digits=10, decimal_places=2)
    bid_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Bid {self.id} - {self.user.username} on {self.product.name}'

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlist')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='wishlisted_by')
    added_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} added {self.product.name} to wishlist'


class UserExtended(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='extended')
    own_store = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
