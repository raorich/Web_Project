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
        return JsonResponse({'error': 'Store already exists.'}, status=400)

#Quit from store
@login_required
def profile_remove_user_store(request):
    user = request.user
    store_pk = request.GET.get('store_id', '')
    user_to_remove_pk = request.GET.get('user_id', '')

    if not store_pk:
        return JsonResponse({'error': 'Missing store_id.'}, status=400)
        
    if not user_to_remove_pk:
        return JsonResponse({'error': 'Missing user_id.'}, status=400)

    store = models.Store.objects.filter(pk=store_pk)
    user_to_remove = models.User.objects.filter(pk=user_to_remove_pk)

    if user_to_remove:
        user_to_remove = user_to_remove.first()
    else:
        return JsonResponse({'error': 'User doesn\'t exists.'}, status=400)

    if store:
        store = store.first()
        users_list = store.users 
        if not user in users_list:
            return JsonResponse({'error': 'This user don\'t own this store.'}, status=400)

        users_list.remove(user_to_remove)
        store.users = users_list
        store.save()

        # if there is no more users, remove the store
        if not users_list:
            store.delete()

        # if the user has no more stores remove own_store
        user_extended = models.UserExtended.objects.get(user=user_to_remove)
        other_stores = models.Store.get_stores_from_user(user_to_remove)
        if not other_stores:
            user_extended.own_store = False
            user_extended.save()
        return JsonResponse({'message': 'Quited from Store successfully.'}, status=200)
    else:
        return JsonResponse({'error': 'Store doesn\'t exists.'}, status=400)

# Remove Store
@login_required
def profile_remove_store(request):
    user = request.user
    store_pk = request.GET.get('store_id', '')

    if not store_pk:
        return JsonResponse({'error': 'Missing store_id.'}, status=400)

    store = models.Store.objects.filter(pk=store_pk)
    
    if store:
        store = store.first()
        users_list = store.users 
        if not user in users_list:
            return JsonResponse({'error': 'This user don\'t own this store.'}, status=400)
        
        for u in users_list:
            users_list.remove(u)
            # if the user has no more stores remove own_store
            user_extended = models.UserExtended.objects.get(user=user)
            other_stores = models.Store.get_stores_from_user(user)
            if not other_stores:
                user_extended.own_store = False
                user_extended.save()
            
        store.users = users_list
        store.save()
        store.delete()
        
        return JsonResponse({'message': 'Store deleted successfully.'}, status=200)
    else:
        return JsonResponse({'error': 'Store doesn\'t exists.'}, status=400)

# Append new user to the store 
@login_required
def profile_add_user_store(request):
    user = request.user
    store_pk = request.GET.get('store_id', '')
    user_to_add_pk = request.GET.get('user_id', '')

    if not store_pk:
        return JsonResponse({'error': 'Missing store_id.'}, status=400)

    if not user_to_add_pk:
        return JsonResponse({'error': 'Missing user_id.'}, status=400)

    store = models.Store.objects.filter(pk=store_pk)
    user_to_add = models.User.objects.filter(pk=user_to_add_pk)

    if user_to_add:
        user_to_add = user_to_add.first()
    else:
        return JsonResponse({'error': 'User doesn\'t exists.'}, status=400)

    if store:
        store = store.first()
        users_list = store.users 
        if not user in users_list:
            return JsonResponse({'error': 'This user don\'t own this store.'}, status=400)
        if user_to_add in users_list:
            return JsonResponse({'error': 'This user already is in this store.'}, status=400)

        users_list.add(user_to_add)
        store.users = users_list
        store.save()

        user_extended = models.UserExtended.objects.get(user=user_to_add)
        user_extended.own_store = True
        user_extended.save()
        return JsonResponse({'message': 'User added to the Store successfully.'}, status=200)
    else:
        return JsonResponse({'error': 'Store doesn\'t exists.'}, status=400)

# Edit name Store
@login_required
def profile_edit_name_store(request):
    user = request.user
    store_pk = request.GET.get('store_id', '')
    new_name = request.GET.get('new_name', '')

    if not store_pk:
        return JsonResponse({'error': 'Missing store_id.'}, status=400)

    store = models.Store.objects.filter(pk=store_pk)

    if store:
        store = store.first()
        users_list = store.users 
        if not user in users_list:
            return JsonResponse({'error': 'This user don\'t own this store.'}, status=400)

        new_name = new_name.strip()
        if len(new_name) <= 5:
            return JsonResponse({'error': 'The new name is too short.'}, status=400)

        try:
            new_name.encode('utf-8')
        except UnicodeEncodeError:
            return JsonResponse({'error': 'Invalid UTF-8 characters in the name.'}, status=400)

        if new_name == store.name:
            return JsonResponse({'error': 'The new name is the same.'}, status=400)

        conflict_store = models.Store.objects.filter(name=new_name)
        if conflict_store:
            return JsonResponse({'error': 'This store already exists'}, status=400)
        
        store.name = new_name
        store.save()

        return JsonResponse({'message': 'User added to the Store successfully.'}, status=200)
    else:
        return JsonResponse({'error': 'Store doesn\'t exists.'}, status=400)

# Edit Product - No esta acabat
@login_required
def profile_edit_product_store(request):
    user = request.user
    store_pk = request.GET.get('store_id', '')
    name = request.GET.get('name', '')
    description = request.GET.get('description', '')
    category = request.GET.get('category', '')
    starting_price = request.GET.get('starting_price', '')
    reserve_price = request.GET.get('reserve_price', '')
    auction_end_time = request.GET.get('auction_end_time', None)
    images = request.GET.get('images', [])

    #filtro segons la categoria

    if not store_pk:
        return JsonResponse({'error': 'Missing store_id.'}, status=400)

    store = models.Store.objects.filter(pk=store_pk)

    if store:
        store = store.first()
        users_list = store.users 
        if not user in users_list:
            return JsonResponse({'error': 'This user don\'t own this store.'}, status=400)

        #FALTA FER FILTROS

        return JsonResponse({'message': 'Product edited successfully.'}, status=200)
    else:
        return JsonResponse({'error': 'Store doesn\'t exists.'}, status=400)


# Create product

# Remove product