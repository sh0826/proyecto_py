from django.contrib import admin
from .models import Boleta
# Register your models here.
class BoletaAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'evento', 'cantidad_boletos', 'precio_boleta')
    search_fields = ('usuario__nombre_completo', 'evento__nombre')

    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj = None):
        return False
    
    def has_delete_permission(self, request, obj = None):
        return False
    
    def has_search_permission(self, request):
        return True
    
admin.site.register(Boleta, BoletaAdmin)