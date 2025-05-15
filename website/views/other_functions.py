import requests
import math
from django.shortcuts import render

def get_quote(request):
    quote = "No se pudo cargar la frase."
    try:
        response = requests.get("https://zenquotes.io/api/random")
        if response.status_code == 200:
            data = response.json()
            quote = f'"{data[0]["q"]}" — {data[0]["a"]}'
    except:
        pass

    return {
        'quote': quote
    }


def paginate_objects(elements, num_featureds=20, page=1):
    if num_featureds > 100: #Max limit
        num_featureds = 100

    page = int(page)
    total_pages = math.ceil(len(elements) / num_featureds)
    if int(total_pages) != total_pages:
        total_pages += 1

    elements = elements[num_featureds*(page-1):num_featureds*page]
    return elements, int(total_pages)