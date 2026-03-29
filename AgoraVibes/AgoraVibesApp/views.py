from django.shortcuts import render
from ReservacionApp.models import Reservacion
from BoletaApp.models import Boleta

# Create your views here.
def inicio(request):
    context = {}
    if request.user.is_authenticated and hasattr(request.user, 'tipo') and request.user.tipo == 3:
        context['reservaciones'] = Reservacion.objects.filter(user=request.user).order_by('-fecha_reservacion')
        context['boletas'] = Boleta.objects.filter(usuario=request.user)
        
    return render(request, "home.html", context)