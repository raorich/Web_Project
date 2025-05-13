from django.shortcuts import render, get_object_or_404
from django.contrib.auth import logout as auth_logout
from django.shortcuts import redirect
from django.http import HttpResponse, JsonResponse

from ..models import Product, Bid, AcquisitionHistory
from .products_functions import get_products_by_auction_end_time, paginate_products

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

def home(request):
    products = get_products_by_auction_end_time()
    products, _ = paginate_products(products, num_featureds=20, page=1)
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


@login_required
def perfil_usuario(request):
    """Vista personalizada para el perfil de usuario"""
    bids = Bid.objects.filter(user=request.user)
    acquisitions = AcquisitionHistory.objects.filter(user=request.user)
    stores = request.user.stores.all()
    return render(request, 'perfil.html', {
        'user': request.user, # Pasa el usuario al template
        'bids': bids,
        'acquisitions': acquisitions,
        'stores': stores
    })
    
    


