from website.models import Watch, Store
from django.conf import settings
from datetime import datetime
from dateutil.relativedelta import relativedelta
import random

import os
import ast
import sys
import csv

# Being on /Web_Project directory
# run with python3 manage.py shell < ./website/scripts/upload/load_watch.py

base_path = settings.BASE_DIR


csv_file_path = os.path.join(base_path, "website", "scripts", "upload", "Watches_data_to_upload.csv")
with open(csv_file_path, mode='r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        try:
            images = ast.literal_eval(row['Imgs'])  # Convert string to list
            images = [ima for ima in images if ima != '']
        except:
            images = []

        Watch.objects.get_or_create(
            ############### Product ##############
            name = row["Header"].strip(),
            category = "watch",
            starting_price = float(row["Price"].strip().replace(" ","")) * (1 - random.randint(5,30)/100),
            reserve_price = float(row["Price"].strip().replace(" ","")),
            auction_end_time = datetime.now().date() + relativedelta(days=random.randint(5,30)), # Reactivar en un altre script afeguint dies
            store = Store.objects.get(pk=1),
            ############### Watch ###############
            brand=row['Brand'].strip(),
            documentation=row['Documentation'].strip(),
            case=row['Case'].strip(),
            model=row['Model'].strip(),
            condition=row['Condition'].strip(),
            year=row['Year'].strip(),
            images=images
        )
