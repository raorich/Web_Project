from django.contrib.auth.models import User
from website.models import UserExtended, Store
import random
import requests

# run with python3 manage.py shell < ./website/scripts/upload/create_random_stores.py

response = requests.get("https://raw.githubusercontent.com/dariusk/corpora/refs/heads/master/data/corporations/fortune500.json")
companies = response.json().get('companies',[])

potential_partners = UserExtended.objects.filter()
user_ids = [ue.user.id for ue in potential_partners]

for _ in range(20):
    num_partners = random.randint(1,6)

    if len(user_ids) < num_partners:
        print(f"No hay suficientes usuarios")
        break

    selected_ids = random.sample(user_ids, num_partners)
    
    for user_id in selected_ids:
        user_extended = UserExtended.objects.get(user__id=user_id)
        user_extended.own_store = True
        user_extended.save()
    
    name = random.choice(companies)
    
    store, created = Store.objects.get_or_create(
        name = name
    )
    if created:
        store.users.add(*User.objects.filter(pk__in=selected_ids))

    companies.remove(name)
