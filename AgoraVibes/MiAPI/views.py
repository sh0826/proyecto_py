from django.shortcuts import render
import requests


def catalogo(request):
    # filter.php?i=vodka ahora devuelve muy pocos resultados; search trae más cócteles.
    url = 'https://www.thecocktaildb.com/api/json/v1/1/search.php?s=vodka'
    drinks = []

    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            payload = response.json()
            drinks = payload.get('drinks') or []
    except requests.RequestException as exc:
        print('Error al conectar con la API:', exc)

    return render(request, 'catalogo_api.html', {'drinks': drinks})
