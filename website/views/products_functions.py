from django.shortcuts import render
from website.models import Product
import random

def get_random_features(num_featureds=20):
    if num_featureds > 100: #Max limit
        num_featureds = 100
    
    max_id = Product.objects.order_by('-id').values_list('id', flat=True).first()

    if max_id <= num_featureds: #DB limit
        num_featureds = max_id

    products = []
    while num_featureds > 0:
        rand_id = random.randint(1,max_id)
        prod = Product.objects.filter(id=rand_id)
        if not prod.exists(): continue

        prod = prod.first()
        if prod in products: continue

        products.append(prod)
        num_featureds -= 1

    return products
