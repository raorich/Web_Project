from django.shortcuts import render
from website.models import Product
from django.http import HttpResponse, JsonResponse
import random
import requests

def get_random_features(num_featureds=20, category=None):
    if num_featureds > 100: #Max limit
        num_featureds = 100

    if category:
        possible_ids = Product.objects.filter(category=category).order_by('-id').values_list('id', flat=True)
    else:
        possible_ids = Product.objects.order_by('-id').values_list('id', flat=True)

    max_id = max(possible_ids)

    if max_id <= num_featureds: #DB limit
        num_featureds = max_id

    products = []
    while num_featureds > 0:
        rand_id = random.randint(0,len(possible_ids)-1)
        object_id = possible_ids[rand_id]
        prod = Product.objects.filter(id=object_id)
        if not prod.exists(): continue

        prod = prod.first()
        if prod in products: continue

        products.append(prod)
        num_featureds -= 1

    return products

#Programación dinamica para las busquedas por ajax
def levenshtein(s1, s2):
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            cost = 0 if s1[i-1] == s2[j-1] else 1
            dp[i][j] = min(
                dp[i-1][j] + 1,      # eliminar
                dp[i][j-1] + 1,      # insertar
                dp[i-1][j-1] + cost  # reemplazar
            )
    return dp[m][n]

def search_products(request):
    TOP = 20
    q = request.GET.get('q', '')
    category = request.GET.get('category', '')

    if not q:
        products = get_random_features(num_featureds=TOP, category=category)
    else:
        products = Product.objects.filter(name__icontains=q)
        if category:
            products = products.filter(category=category)

        #Sirve para obtener el mejor match possible
        def rank(product):
            return levenshtein(q, product.name.lower())
        products = sorted(products, key=rank)[:TOP]

    html = render(request, 'components/product_cards_ajax.html', {'products': products, 'current_query': q}).content.decode('utf-8')
    return JsonResponse({'html': html})


def pujar_producto(request, product_id):
    return HttpResponse(f"Has llegado a la página de puja del producto con ID {product_id}")
