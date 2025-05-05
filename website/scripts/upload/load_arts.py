from website.models import Art, Store
from django.conf import settings
from datetime import datetime
from dateutil.relativedelta import relativedelta
import random

import os
import ast
import sys
import csv

# Being on /Web_Project directory
# run with python3 manage.py shell < ./website/scripts/upload/load_arts.py

base_path = settings.BASE_DIR


csv_file_path = os.path.join(base_path, "website", "scripts", "upload", "Art_data_to_upload.csv")

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

        price = float(row["Price"].strip())

        specifications = row['Specifications'].strip()
        split_specs = specifications.split(' • ')
        
        country = ''
        technique = ''
        if len(split_specs) == 1:
            year = split_specs[0]
        elif len(split_specs) == 2:
            year, country = split_specs
        elif len(split_specs) >= 3:
            year, country, technique = split_specs

        try:
            year = int(year.strip())
        except Exception as e:
            year = 1999

        artist = row['Artist'].strip()
        dimensions = row['Dimensions']

        description = [artist, country] 
        if technique:
            description += [technique.split(',')[0]]
    
        Art.objects.get_or_create(
            ############### Product ##############
            name = row["Header"].strip(),
            description = " | ".join(description),
            category = "art",
            starting_price = price * (1 - random.randint(5,30)/100),
            reserve_price = price,
            auction_end_time = datetime.now().date() + relativedelta(days=random.randint(5,30)), # Reactivar en un altre script afeguint dies
            store = Store.objects.get(pk=store_selected),
            images=images,
            ############### Art ###############
            artist = artist,
            technique = technique,
            country = country,
            dimensions = dimensions,
            year=year
        )
