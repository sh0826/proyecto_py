from django.shortcuts import render,redirect
from . import models
from .forms import ReservacionForm
# Create your views here.
def reservacion(request):
    reservaciones=models.reservacion.objects.all()
    return render(request,'reservacion.html',{'reservacion':reservaciones})
def crear_reserva(request):
    if request.method == "POST":
        form = ReservacionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("reservas") 
    else:
        form = ReservacionForm()

    return render(request, "crear_reserva.html", {"form": form})