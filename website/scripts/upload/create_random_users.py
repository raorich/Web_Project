from django.contrib.auth.models import User
from website.models import UserExtended, Store
from django.conf import settings
from pprint import pprint
import requests
import sys

# Being on /Web_Project directory
# run with python3 manage.py shell < ./website/scripts/upload/create_random_users.py

#create x users

for _ in range(100):

    response = requests.get('https://randomuser.me/api/')
    json_user = response.json()
    results = json_user.get('results',[None])[0]

    user = User.objects.create_user(
        username=results['login']['username'],
        email=results['email'],
        password=results['login']['salt'],
        first_name=results['name']['first'],
        last_name=results['name']['last']
    )

    UserExtended.objects.get_or_create(
        user=user,
        own_store=False,
    )
