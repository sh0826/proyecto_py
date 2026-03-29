from django.shortcuts import render
from .models import Boleta
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
from django.http import HttpResponse
from django.http import HttpResponseForbidden
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect, get_object_or_404
from django.views import View
from django.db.models import Sum 
from django.core.exceptions import ValidationError
from EventoApp.models import Evento
# Create your views here.
class lista(LoginRequiredMixin, ListView):
    model= Boleta
    template_name = 'boleta.html'
    context_object_name = 'boletas'

    def get_queryset(self):
        if self.request.user.tipo == 3:
            return  Boleta.objects.filter(usuario=self.request.user)
        return Boleta.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['eventos'] = Evento.objects.all()
        return context
class crear(LoginRequiredMixin, CreateView):
    model = Boleta
    fields = ["cantidad_boletos","evento"]
    template_name = 'formulario.html'
    success_url = reverse_lazy('lista')

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.tipo != 3:
            return HttpResponseForbidden("Solo clientes")
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        evento = form.instance.evento
        cantidad = form.instance.cantidad_boletos

        # VALIDAR CUPOS
        if cantidad > evento.cupos_disponibles():
            form.add_error(None, "No hay más espacio para este evento 😸")
            return self.form_invalid(form)

        # GUARDAR DATOS
        form.instance.usuario = self.request.user
        form.instance.precio_boleta = evento.precio_boleta * cantidad

        return super().form_valid(form)
     
class actualizar(LoginRequiredMixin, UpdateView):
    model = Boleta
    fields = ["cantidad_boletos"    ,"evento"]
    template_name = 'formulario.html'
    success_url = reverse_lazy('lista')

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.tipo != 3 :
            return HttpResponseForbidden("Solo clientes")
        return super().dispatch(request, *args, **kwargs)   
    
    def form_valid(self, form):
        form.instance.usuario = self.request.user
        form.instance.precio_boleta = (
            form.instance.evento.precio_boleta * form.instance.cantidad_boletos
        )
        return super().form_valid(form)
    def form_valid(self, form):
        evento = form.instance.evento
        cantidad = form.instance.cantidad_boletos

        if cantidad > evento.cupos_disponibles():
            form.add_error(None, "No hay más espacio para este evento 😸")
            return self.form_invalid(form)

        form.instance.usuario = self.request.user
        form.instance.precio_boleta = evento.precio_boleta * cantidad

        return super().form_valid(form)

class eliminar(LoginRequiredMixin, View):
    def get(self, request, pk):
        if self.request.user.tipo != 3:
            return HttpResponseForbidden("Solo clientes")

        boleta = get_object_or_404(
            Boleta,
            pk=pk,
            usuario=request.user
        )
        boleta.delete()
        return redirect('lista')
    