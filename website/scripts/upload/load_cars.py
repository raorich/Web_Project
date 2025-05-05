from website.models import Automobile, Store
from django.conf import settings
from datetime import datetime
from dateutil.relativedelta import relativedelta
import random

import os
import ast
import sys
import csv

# Being on /Web_Project directory
# run with python3 manage.py shell < ./website/scripts/upload/load_cars.py

base_path = settings.BASE_DIR


csv_file_path = os.path.join(base_path, "website", "scripts", "upload", "Cars_data_to_upload.csv")

max_store = len(Store.objects.all())

with open(csv_file_path, mode='r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        try:
            images = ast.literal_eval(row['Imgs'])  # Convert string to list
            images = [ima for ima in images if ima != '']
        except:
            images = []

        if max_store <= 0:
            print("There are no stores")
            break
        
        store_selected = random.randint(1,max_store-1)
        price = row["Price"].strip().replace("$","").replace("(OBO)","").replace(",","") 
        if price == "Contact Seller":
            price = random.randint(400000,600000)
        price = float(price)

        make = row['Brand'].strip()
        model = row['Model'].strip()
        restoration = row['Restoration'].strip() or "Unrestored"
        exterior_color = row['Exterior Color'].strip().title()
        transmission = row['Transmission'].strip()
        
        engine_condition = row['Engine Condition'].strip()
        sp_engine = engine_condition.split("-")
        if sp_engine[0] == "":
            sp_engine[0] = "Original"
        if sp_engine[1] == "":
            sp_engine[1] = ["Not Running", "Malfunction"][random.randint(0,1)]
        engine_condition = f"{sp_engine[0].strip()} - {sp_engine[1].strip()}"
    
        Automobile.objects.get_or_create(
            ############### Product ##############
            name = row["Header"].strip()[5:],
            description = " | ".join([make,transmission,exterior_color]),
            category = "automobile",
            starting_price = price * (1 - random.randint(5,30)/100),
            reserve_price = price,
            auction_end_time = datetime.now().date() + relativedelta(days=random.randint(5,30)), # Reactivar en un altre script afeguint dies
            store = Store.objects.get(pk=store_selected),
            images=images,
            ############### Watch ###############
            make = make,
            model = model,
            restoration = restoration,
            exterior_color = exterior_color,
            transmission = transmission,
            engine_condition = engine_condition,
            year=row['Year'].strip()
        )
