from django.shortcuts import render
from .models import Boleta
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
from django.http import HttpResponse
# Create your views here.
class lista(ListView):
    model= Boleta
    template_name = 'boleta.html'
    context_object_name = 'boletas'

class nueva(CreateView):
    model = Boleta
    fields = ['precio_boleta','cantidad_boletos','usuario','evento']
    template_name = 'crear.html'

class actualizar(UpdateView):
    model = Boleta
    fields = ['precio_boleta','cantidad_boletos','usuario','evento']
    template_name = 'crear.html'

class eliminar(DeleteView):
    model = Boleta
    template_name = "eliminar.html"