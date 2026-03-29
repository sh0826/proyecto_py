from django.shortcuts import render
from .models import Evento
from django.views.generic import ListView
from django.db.models import Sum
# Create your views here.
class lis_eventos(ListView):
    model = Evento
    template_name = 'evento.html'
    context_object_name = 'eventos'