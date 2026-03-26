
from django.db import models
from AgoraVibes import settings

# Create your models here.
class reservacion(models.Model):
    id_reservacion= models.AutoField(primary_key=True)
    user= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    cantidad_personas= models.IntegerField()
    cantidad_mesas= models.IntegerField()
    fecha_reservacion= models.DateField()
    ocasion= models.CharField(max_length=100, null=True, blank=True)

def __str__(self):
    return f"Reservacion{self.user}"