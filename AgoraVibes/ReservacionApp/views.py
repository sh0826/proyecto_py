from django.shortcuts import render, redirect, get_object_or_404
from . import models
from .forms import ReservacionForm
from django.contrib import messages
# Vista para listar las reservas del usuario
def reservacion(request):
    reservaciones = models.Reservacion.objects.filter(user=request.user)
    return render(request, 'reservacion.html', {'reservaciones': reservaciones})

# Vista para crear una nueva reserva
def crear_reserva(request):
    if request.method == "POST":
        form = ReservacionForm(request.POST, user=request.user)  # Pasamos el usuario al formulario
        if form.is_valid():
            reservacion = form.save(commit=False)
            reservacion.user = request.user  # Asignamos el usuario antes de guardar
            reservacion.save()
            messages.success(request, "Reservación creada exitosamente.")
            return redirect("reservacion")
        else:
            print(form.errors)  # Para depurar errores de validación
    else:
        form = ReservacionForm(user=request.user)  # Formulario vacío en GET

    return render(request, "crear_reserva.html", {"form": form})

# Vista para editar una reserva existente
def editar_reserva(request, id):
    reservacion = get_object_or_404(models.Reservacion, id=id)

    # Solo el propietario puede editar
    if reservacion.user != request.user:
        return redirect("reservacion")

    if request.method == "POST":
        form = ReservacionForm(request.POST, instance=reservacion, user=request.user)
        if form.is_valid():
            form.save()
            return redirect("reservacion")
    else:
        form = ReservacionForm(instance=reservacion, user=request.user)  # En GET pasamos solo el instance y el user

    return render(request, "editar_reserva.html", {"form": form})

# Vista para eliminar una reserva
def eliminar_reserva(request, id):
    reservacion = get_object_or_404(models.Reservacion, id=id)

    # Solo el propietario puede eliminar
    if reservacion.user != request.user:
        return redirect("reservacion")

    if request.method == "POST":
        reservacion.delete()
        return redirect("reservacion")

    return render(request, "eliminar_reserva.html", {"reservacion": reservacion})