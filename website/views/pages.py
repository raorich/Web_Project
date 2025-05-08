from django.shortcuts import render, get_object_or_404
from django.contrib.auth import logout as auth_logout
from django.shortcuts import redirect
<<<<<<< Updated upstream
from ..models import Product
from .products_functions import get_random_features
from django.http import HttpResponse, JsonResponse
=======

from .products_functions import get_random_features, get_quote
>>>>>>> Stashed changes


def home(request):
    products = get_random_features(20)
<<<<<<< Updated upstream
    from pprint import pprint
    pprint([product.name for product in products])
    return render(request, 'home.html', {"products": products})

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

def search_products(request):
    q = request.GET.get('q', '')
    products = Product.objects.filter(name__icontains=q)[:12]
    html = render(request, 'components/product_cards_ajax.html', {'products': products}).content.decode('utf-8')
    return JsonResponse({'html': html})

def pujar_producto(request, product_id):
    return HttpResponse(f"Has llegado a la página de puja del producto con ID {product_id}")
=======
    quote = get_quote()
    return render(request, 'home.html', {"products": products, "quote": quote})
    


>>>>>>> Stashed changes
