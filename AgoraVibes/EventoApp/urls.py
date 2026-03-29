from django.urls import path
from .views import lis_eventos 

urlpatterns = [
    path('eventos/', lis_eventos.as_view(), name='eventos'),
]
