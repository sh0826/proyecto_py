from django.shortcuts import render,redirect,get_object_or_404
from . import models
from .forms import ReservacionForm
# Create your views here.
def reservacion(request):
    reservaciones=models.Reservacion.objects.filter(user=request.user)
    
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
def editar_reserva(request, id):
    reservacion = get_object_or_404(models.Reservacion, id=id)

    if reservacion.user != request.user:
            return redirect("reservacion")
    if request.method == "POST":
        form = ReservacionForm(request.POST, instance=reservacion)
        if form.is_valid():
            form.save()
            return redirect("reservacion")
    else:
        form = ReservacionForm(instance=reservacion)

    return render(request, "editar_reserva.html", {"form": form})
def eliminar_reserva(request, id):
    reservacion = get_object_or_404(models.Reservacion, id=id)
    if reservacion.user != request.user:
            return redirect("reservacion")
    if request.method == "POST":
        reservacion.delete()
        return redirect("reservacion")

    return render(request, "eliminar_reserva.html", {"reservacion": reservacion})