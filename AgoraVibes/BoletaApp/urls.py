from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista.as_view(), name='lista'),
    path('nueva/', views.crear.as_view(), name='crear'),
    path('actualizar/<int:pk>', views.actualizar.as_view(), name='actualizar'),
    path('eliminar/<int:pk>', views.eliminar.as_view(), name='eliminar'),    
    path('listar/', views.lista.as_view(), name='listar'),
]
