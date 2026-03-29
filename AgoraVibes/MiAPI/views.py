from django.shortcuts import render
import requests
import http.client

    # Create your views here.
def catalogo(request):
    url = 'https://www.thecocktaildb.com/api/json/v1/1/filter.php?i=Vodka'
    response = requests.get(url)
    data = []
    if response.status_code == 200:
        data = response.json()
    else:
        print('Error al conectar:', response.status_code)   
    return render(request, "catalogo.html", {"datos": data})