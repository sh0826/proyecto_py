from django.urls import path
from . import views

urlpatterns = [
    path('', views.reservacion, name='reservacion'),
    path('crear/', views.crear_reserva,name='crear_reseva'),
    path('editar/<int:id>/', views.editar_reserva, name='editar_reserva'),
    path('eliminar/<int:id>/', views.eliminar_reserva, name='eliminar_reserva')
    ]
