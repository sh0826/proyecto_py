from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name="inicio"),    #Apunta al directorio raíz del sitio    
]