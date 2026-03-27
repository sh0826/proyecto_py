from django.shortcuts import render,redirect
from . import models
from .forms import ReservacionForm
# Create your views here.
def reservacion(request):
    reservaciones=models.Reservacion.objects.all()
    return render(request,'reservacion.html',{'reservaciones':reservaciones})
def crear_reserva(request):
    if request.method == "POST":
        form = ReservacionForm(request.POST)
        if form.is_valid():
            reservaciones = form.save(commit=False) 
            reservaciones.user=request.user
            reservaciones.save()
            
            return redirect("reservacion") 
    else:
        form = ReservacionForm()

    return render(request, "crear_reserva.html", {"form": form})