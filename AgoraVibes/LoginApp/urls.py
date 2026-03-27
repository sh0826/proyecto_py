from django.urls import path
from . import views

urlpatterns = [
    path('registro/', views.registrar_usuario, name='registro'),
    path('login/', views.iniciar_sesion, name='login'),
    path('cerrar_sesion/', views.cerrar_sesion, name='cerrar_sesion'),
    path('recuperar/', views.recuperar,  name='recuperar'),
    path('cambiar_contraseña/', views.cambiar_contraseña, name='cambiar_contraseña')
    ]