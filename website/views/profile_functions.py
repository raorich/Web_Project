from django.shortcuts import render, redirect
from django.utils import timezone
from website import models
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required

from .other_functions import paginate_objects

from datetime import datetime
from decimal import Decimal

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
    html = render(request, 'components/history_acquision_stores_ajax.html', {'acquisition': acquisition_history}).content.decode('utf-8')
    return JsonResponse({
            'html': html,
            'total_pages': total_pages
        })

####

# Create Store
@login_required
def profile_create_store(request):
    user = request.user
    name_store = request.GET.get('store_name', '')

    if not name_store:
        return JsonResponse({'error': 'Missing store name.'}, status=400)

    store, created = models.Store.objects.get_or_create(name=name_store)

    if created:
        store.users.add(user)
        user_extended, u_created = models.UserExtended.objects.get_or_create(user=user)
        user_extended.own_store = True
        user_extended.save()

        return redirect('perfil')
        # return JsonResponse({'message': 'Store created successfully.'}, status=200)
    else:
        return JsonResponse({'error': 'Store already exists.'}, status=400)

#Quit from store
@login_required
def profile_remove_user_store(request):
    user = request.user
    store_pk = request.GET.get('store_id', '')
    username_to_remove = request.GET.get('user_username', '')

    try:
        user_to_remove = models.User.objects.get(username=username_to_remove)
        user_to_remove_pk = user_to_remove.id
    except models.User.DoesNotExist:
        return JsonResponse({'error': 'User doesn\'t exist.'}, status=400)

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
        if not user in store.users.all():
            return JsonResponse({'error': 'This user don\'t own this store.'}, status=400)

        store.users.remove(user_to_remove)
        store.save()

        # if there is no more users, remove the store
        if not users_list:
            store.delete()

        # if the user has no more stores remove own_store
        user_extended = models.UserExtended.objects.filter(user=user_to_remove)
        if user_extended:
            user_extended = user_extended.first()
            other_stores = models.Store.get_stores_from_user(user_to_remove)
            if not other_stores:
                user_extended.own_store = False
                user_extended.save()

        return redirect('perfil')
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

        if not user in store.users.all():
            return JsonResponse({'error': 'This user don\'t own this store.'}, status=400)

        for u in store.users.all():
            store.users.remove(u)
            user_extended = models.UserExtended.objects.filter(user=u)
            print(user_extended)
            if user_extended:
                user_extended = user_extended.first()
                other_stores = models.Store.get_stores_from_user(u)
                if not other_stores:
                    user_extended.own_store = False
                    user_extended.save()
            
        store.users.clear()
        store.save()
        store.delete()

        return redirect('perfil')
        # return JsonResponse({'message': 'Store deleted successfully.'}, status=200)
    else:
        return JsonResponse({'error': 'Store doesn\'t exists.'}, status=400)

# Append new user to the store 
@login_required
def profile_add_user_store(request):
    user = request.user
    store_pk = request.GET.get('store_id', '')
    username_to_add = request.GET.get('user_username', '')

    if not username_to_add:
        return JsonResponse({'error': 'Missing username.'}, status=400)

    try:
        user_to_add = models.User.objects.get(username=username_to_add)
        user_to_add_pk = user_to_add.id
    except models.User.DoesNotExist:
        return JsonResponse({'error': 'User doesn\'t exist.'}, status=400)

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

        if not user in store.users.all():
            return JsonResponse({'error': 'This user don\'t own this store.'}, status=400)
        if user_to_add in store.users.all():
            return JsonResponse({'error': 'This user already is in this store.'}, status=400)

        store.users.add(user_to_add)
        store.save()
        user_extended, create = models.UserExtended.objects.get_or_create(user=user_to_add)
        user_extended.own_store = True
        user_extended.save()

        return redirect('perfil')
        # return JsonResponse({'message': 'User added to the store successfully.'}, status=200)
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
        if not user in store.users.all():
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

        return redirect('perfil')
        # return JsonResponse({'message': 'Store name edited successfully.'}, status=200)
    else:
        return JsonResponse({'error': 'Store doesn\'t exists.'}, status=400)


def check_product_fields(request):
    json_field = {}

    # Helper para validar campos obligatorios
    def require(field, name):
        if field is None or field == '':
            return False, f'El campo "{name}" es obligatorio'
        return True, None

    # Helper para convertir a decimal
    def to_decimal(value, name):
        if value is None:
            return None
        try:
            return Decimal(value)
        except:
            raise ValueError(f'El campo "{name}" debe ser un número decimal')

    # Helper para convertir a datetime
    def to_datetime(value, name):
        if value is None:
            return None
        try:
            return datetime.fromisoformat(value)
        except:
            raise ValueError(f'El campo "{name}" debe estar en formato ISO 8601')

    try:
        # Campos obligatorios
        name = request.GET.get('name', None) or None
        ok, msg = require(name, 'name')
        if not ok: return (False, msg), {}

        description = request.GET.get('description', None) or None
        ok, msg = require(description, 'description')
        if not ok: return (False, msg), {}

        category = request.GET.get('category', None) or None
        ok, msg = require(category, 'category')
        if not ok: return (False, msg), {}

        starting_price_raw = request.GET.get('starting_price', None) or None
        ok, msg = require(starting_price_raw, 'starting_price')
        if not ok: return (False, msg), {}
        starting_price = to_decimal(starting_price_raw, 'starting_price')

        reserve_price_raw = request.GET.get('reserve_price', None) or None
        ok, msg = require(reserve_price_raw, 'reserve_price')
        if not ok: return (False, msg), {}
        reserve_price = to_decimal(reserve_price_raw, 'reserve_price')

        if reserve_price < starting_price:
            return (False, "reserve_price must be higher than starting_price"), {}

        auction_end_time_raw = request.GET.get('auction_end_time', None) or None
        ok, msg = require(auction_end_time_raw, 'auction_end_time')
        if not ok: return (False, msg), {}
        auction_end_time = to_datetime(auction_end_time_raw, 'auction_end_time')

        images = request.GET.get('images', []) or None
        if isinstance(images, str):
            images = images.split(',') if images else None
        ok, msg = require(images, 'auction_end_time')
        if not ok: return (False, msg), {}

        json_field.update({
            'name': name,
            'description': description,
            'category': category,
            'starting_price': starting_price,
            'reserve_price': reserve_price,
            'auction_end_time': auction_end_time,
            'images': images
        })

        # Comunes
        year = request.GET.get('year', None) or None
        model = request.GET.get('model', None) or None

        json_field['year'] = year
        json_field['model'] = model

        # Categoría específica
        if category == 'watch':
            json_field['brand'] = request.GET.get('brand', None) or None
            json_field['documentation'] = request.GET.get('documentation', None) or None
            json_field['case'] = request.GET.get('case', None) or None
            json_field['condition'] = request.GET.get('condition', None) or None

        elif category == 'art':
            json_field['artist'] = request.GET.get('artist', None) or None
            json_field['technique'] = request.GET.get('technique', None) or None
            json_field['country'] = request.GET.get('country', None) or None
            json_field['dimensions'] = request.GET.get('dimensions', None) or None

        elif category == 'automobiles':
            json_field['make'] = request.GET.get('make', None) or None
            json_field['restoration'] = request.GET.get('restoration', None) or None
            json_field['transmission'] = request.GET.get('transmission', None) or None
            json_field['exterior_color'] = request.GET.get('exterior_color', None) or None
            json_field['engine_condition'] = request.GET.get('engine_condition', None) or None

        else:
            return (False, f'La categoría "{category}" no es válida'), {}

        return (True, 'Valid'), json_field

    except ValueError as e:
        return (False, str(e)), {}
    

# Edit Product
@login_required
def profile_edit_product_store(request):
    user = request.user
    store_pk = request.GET.get('store_id', '')
    product_pk = request.GET.get('product_id', '')
    
    (valid, message), json_field = check_product_fields(request)
    if not valid:
        return JsonResponse({'error': message}, status=400)

    if not store_pk:
        return JsonResponse({'error': 'Missing store_id.'}, status=400)

    store = models.Store.objects.filter(pk=store_pk)

    if store:
        store = store.first()
        if not user in store.users.all():
            return JsonResponse({'error': 'This user don\'t own this store.'}, status=400)

        product = None
        category = json_field.get('category')

        try:
            if category == 'watch':
                product = models.Watch.objects.get(pk=product_pk, store=store)
            elif category == 'art':
                product = models.Art.objects.get(pk=product_pk, store=store)
            elif category == 'automobiles':
                product = models.Automobile.objects.get(pk=product_pk, store=store)
            else:
                return JsonResponse({'error': f'Unknown category: {category}'}, status=400)
        except models.Product.DoesNotExist:
            return JsonResponse({'error': 'Product not found in this store.'}, status=400)
        
        for key, value in json_field.items():
            if hasattr(product, key):
                setattr(product, key, value)

        product.save()
        
        return JsonResponse({'message': 'Product edited successfully.'}, status=200)
    else:
        return JsonResponse({'error': 'Store doesn\'t exists.'}, status=400)


# Create product
@login_required
def profile_create_product_store(request):
    user = request.user
    store_pk = request.GET.get('store_id', '')
    
    (valid, message), json_field = check_product_fields(request)
    if not valid:
        return JsonResponse({'error': message}, status=400)

    if not store_pk:
        return JsonResponse({'error': 'Missing store_id.'}, status=400)

    store = models.Store.objects.filter(pk=store_pk)

    if store:
        store = store.first()
        if not user in store.users.all():
            return JsonResponse({'error': 'This user doesn\'t own this store.'}, status=400)

        category = json_field.get('category')
        name = json_field.get('name')

        if not name:
            return JsonResponse({'error': 'Product name is required for creation.'}, status=400)

        json_field['store'] = store
        product = None
        created = False

        try:
            if category == 'watch':
                product, created = models.Watch.objects.get_or_create(name=name, store=store, defaults={})
            elif category == 'art':
                product, created = models.Art.objects.get_or_create(name=name, store=store, defaults={})
            elif category == 'automobiles':
                product, created = models.Automobile.objects.get_or_create(name=name, store=store, defaults={})
            else:
                return JsonResponse({'error': f'Unknown category: {category}'}, status=400)
        except Exception as e:
            return JsonResponse({'error': f'Error during get_or_create: {str(e)}'}, status=500)

        # Asignar campos que existan
        for key, value in json_field.items():
            if hasattr(product, key):
                setattr(product, key, value)

        product.save()

        message = 'Product created successfully.' if created else 'Product updated successfully.'
        return JsonResponse({'message': message}, status=200)
    else:
        return JsonResponse({'error': 'Store doesn\'t exists.'}, status=400)

# Remove product
@login_required
def profile_remove_product_store(request):
    user = request.user
    store_pk = request.GET.get('store_id', '')
    product_pk = request.GET.get('product_id', '')
    
    if not store_pk:
        return JsonResponse({'error': 'Missing store_id.'}, status=400)

    store = models.Store.objects.filter(pk=store_pk)

    if store:
        store = store.first()
        if not user in store.users.all():
            return JsonResponse({'error': 'This user doesn\'t own this store.'}, status=400)

        try:
            product = models.Product.objects.get(pk=product_pk)
            product.delete()
        except models.User.DoesNotExist:
            return JsonResponse({'error': 'Product doesn\'t exist.'}, status=400)

        return JsonResponse({'message': 'Product removed successfully.'}, status=200)
    else:
        return JsonResponse({'error': 'Store doesn\'t exists.'}, status=400)