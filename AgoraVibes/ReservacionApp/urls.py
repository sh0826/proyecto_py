from django.urls import path
from . import views

urlpatterns = [
    path('', views.reservacion, name='reservacion'),
    path('crear/', views.crear_reserva,name='crear_reseva')
    ]
