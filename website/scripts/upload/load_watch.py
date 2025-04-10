from website.models import Watch
from django.conf import settings
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
        except:
            images = []

        Watch.objects.get_or_create(
            brand=row['Brand'],
            documentation=row['Documentation'],
            case=row['Case'],
            model=row['Model'],
            condition=row['Condition'],
            year=int(row['Year']),
            images=images
        )
