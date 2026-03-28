from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista.as_view(), name='lista'),
    path('nueva/', views.nueva.as_view(), name='nueva'),
    path('actualizar/<int:pk>', views.actualizar.as_view(), name='actualizar'),
    path('eliminar/<int:pk>', views.eliminar.as_view(), name='eliminar'),    
    path('listar/', views.lista.as_view(), name='listar'),
]
