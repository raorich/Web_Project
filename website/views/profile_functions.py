from django.shortcuts import render
from django.utils import timezone
from website import models
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required

from .other_functions import paginate_objects

import random
import requests
import time

@login_required
def profile_bids(request):
    TOP = 5
    user = request.user
    page = request.GET.get('page',1)
    total_pages = 1

    bids = models.Bid.objects.filter(user=user)
    bids, total_pages = paginate_objects(bids, num_featureds=TOP, page=page)
    html = render(request, 'components/table_bids_ajax.html', {'bids': bids}).content.decode('utf-8')
    return JsonResponse({
            'html': html,
            'total_pages': total_pages
        })

@login_required
def profile_stores(request):
    TOP = 5
    user = request.user
    page = request.GET.get('page',1)
    total_pages = 1

    stores = models.Store.get_stores_from_user(user)
    stores, total_pages = paginate_objects(stores, num_featureds=TOP, page=page)
    html = render(request, 'components/table_stores_ajax.html', {'stores': stores}).content.decode('utf-8')
    return JsonResponse({
            'html': html,
            'total_pages': total_pages
        })

@login_required
def profile_history_acquision(request):
    TOP = 5
    user = request.user
    page = request.GET.get('page',1)
    total_pages = 1

    acquisition_history = models.AcquisitionHistory.objects.filter(user=user)
    acquisition_history, total_pages = paginate_objects(acquisition_history, num_featureds=TOP, page=page)
    html = render(request, 'components/table_history_acquision_ajax.html', {'acquisition': acquisition_history}).content.decode('utf-8')
    return JsonResponse({
            'html': html,
            'total_pages': total_pages
        })

####

# Create Store
@login_required
def profile_create_store(request):
    user = request.user
    name_store = request.GET.get('name', '')

    if not name_store:
        return JsonResponse({'error': 'Missing store name.'}, status=400)

    store, created = models.Store.objects.get_or_create(name=name_store)

    if created:
        store.users.add(user)
        user_extended = models.UserExtended.objects.get(user=user)
        user_extended.own_store = True
        user_extended.save()
        return JsonResponse({'message': 'Store created successfully.'}, status=200)
    else:
        return JsonResponse({'message': 'Store already exists.'}, status=400)

# Remove Store # SEGURETAT L'USUARI HA d'estar dins de la store

# Append new user to the store 

# Edit Store

# Edit Product

# Create product

# Remove product

# Edit product