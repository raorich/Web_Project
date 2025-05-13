import requests
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