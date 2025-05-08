from django.shortcuts import render, get_object_or_404
from django.contrib.auth import logout as auth_logout
from django.shortcuts import redirect
from django.http import HttpResponse, JsonResponse

from ..models import Product
from .products_functions import get_random_features
from .other_functions import get_quote




def home(request):
    products = get_random_features(20)
    quote = get_quote()
    return render(request, 'home.html', {"products": products, "quote": quote})

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # Detectar tipo específico
    subproduct = product
    product_type = 'generic'

    if hasattr(product, 'watch'):
        subproduct = product.watch
        product_type = 'watch'
    elif hasattr(product, 'art'):
        subproduct = product.art
        product_type = 'art'
    elif hasattr(product, 'automobile'):
        subproduct = product.automobile
        product_type = 'automobile'

    return render(request, 'components/product_detail.html', {
        'product': subproduct,
        'type': product_type  # ← Esto es lo que faltaba
    })
    
    


