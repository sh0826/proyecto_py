from django.contrib import admin
from .models import Usuario

class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('numero_documento', 'nombre_completo', 'correo')

admin.site.register(Usuario, UsuarioAdmin)
# Register your models here.
