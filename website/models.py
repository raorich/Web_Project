from django.db import models
from django.contrib.auth.models import User, Group
from django.urls import reverse
from django.utils.timezone import now

# Our data base model
class Store(models.Model):
    name = models.CharField(max_length=255, blank = False, unique = True)
    users = models.ManyToManyField(User, related_name='stores')

    def __str__(self):
        return self.name
    
    @classmethod
    def get_stores_from_user(cls, user):
        return cls.objects.filter(users=user)
    
    
class Product(models.Model):
    name = models.CharField(max_length=255, blank = False)
    description = models.CharField(max_length=255, blank = False)
    category = models.CharField(max_length=100, blank = False) # art, automobiles, watch
    starting_price = models.DecimalField(max_digits=10, decimal_places=2)
    reserve_price = models.DecimalField(max_digits=10, decimal_places=2)
    auction_end_time = models.DateTimeField()
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='products', default=1)
    images = models.JSONField(default=list, blank=True)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('product_detail', args=[str(self.id)])

    @property
    def is_expired(self):
        return self.auction_end_time < now()

class AcquisitionHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='acquisition_history')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.product.name} on {self.date}'

class Watch(Product):
    brand = models.CharField(max_length=100, default='')
    documentation = models.CharField(max_length=255, default='')
    case = models.CharField(max_length=255, default = '')
    model = models.CharField(max_length=100, default = '')
    condition = models.CharField(max_length=100, default = '')
    year = models.CharField(max_length=100, default = '')

class Art(Product):
    artist = models.CharField(max_length=100, default = '')
    technique = models.CharField(max_length=100, default = '')
    country = models.CharField(max_length=100, default = '')
    dimensions = models.CharField(max_length=100, default = '')
    year = models.IntegerField()

class Automobile(Product):
    make = models.CharField(max_length=100, default = '')
    model = models.CharField(max_length=100, default = '')
    restoration = models.CharField(max_length=100, default = '')
    transmission = models.CharField(max_length=100, default = '')
    exterior_color = models.CharField(max_length=100, default = '')
    engine_condition = models.CharField(max_length=100, default = '')
    year = models.CharField(max_length=100, default = '')

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
