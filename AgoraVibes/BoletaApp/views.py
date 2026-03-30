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
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
# Create your views here.
class lista(LoginRequiredMixin, ListView):
    model= Boleta
    template_name = 'boleta.html'
    context_object_name = 'boletas'

    def get_queryset(self):
        queryset = Boleta.objects.all()

        if self.request.user.tipo == 3:
            queryset = queryset.filter(usuario=self.request.user)
        
        evento_id = self.request.GET.get('evento')
        if evento_id:
            queryset = queryset.filter(evento_id = evento_id)

        cantidad = self.request.GET.get('cantidad')
        if cantidad: 
            queryset = queryset.filter(cantidad_boletos = cantidad) 
        return queryset

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

            if cantidad > evento.cupos_disponibles():
                form.add_error(None, "No hay más espacio para este evento")
                return self.form_invalid(form)

            form.instance.usuario = self.request.user
            form.instance.precio_boleta = evento.precio_boleta * cantidad

            return super().form_valid(form)
     
class actualizar(LoginRequiredMixin, UpdateView):
    model = Boleta
    fields = ["cantidad_boletos","evento"]
    template_name = 'formulario.html'
    success_url = reverse_lazy('lista')

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.tipo != 3:
            return HttpResponseForbidden("Solo clientes")
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        boleta = self.get_object()
        evento = form.instance.evento

        cantidad_anterior = boleta.cantidad_boletos
        nueva_cantidad = form.instance.cantidad_boletos

        diferencia = nueva_cantidad - cantidad_anterior

        if diferencia > evento.cupos_disponibles():
            form.add_error(None, "No hay más espacio para este evento")
            return self.form_invalid(form)
        
        form.instance.usuario = self.request.user
        form.instance.precio_boleta = evento.precio_boleta * nueva_cantidad
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
    
class generar_pdf(LoginRequiredMixin, View):
    def get(self, request, pk):
        boleta = get_object_or_404(Boleta, pk = pk)
        
        if boleta.usuario != request.user:
            return HttpResponseForbidden("No tienes permiso")
        
        response = HttpResponse(content_type ='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="Boleta.pdf"'

        p = canvas.Canvas(response, pagesize=letter)
    
        p.setFont("Helvetica",12)
        p.drawString(100, 750, "BOLETA - AGORA VIBES")
        p.drawString(100,720, f"Usuario: {boleta.usuario}")
        p.drawString(100,700,f"Evento: { boleta.evento}")
        p.drawString(100, 680, f"Cantidad: {boleta.cantidad_boletos}")
        p.drawString(100, 660, f"Total: {boleta.precio_boleta}")

        p.save()
        return response