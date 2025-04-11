from django.shortcuts import render
from django.contrib.auth import logout as auth_logout
from django.shortcuts import redirect

from .products_functions import get_random_features


def home(request):
    products = get_random_features(20)
    from pprint import pprint
    pprint([product.name for product in products])
    return render(request, 'home.html', {"products": products})
