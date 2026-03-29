from django.contrib import admin
from .models import Reservacion
# Register your models here.
class ReservacionAdmin(admin.ModelAdmin):
    list_display = ('user', 'cantidad_personas', 'cantidad_mesas', 'fecha_reservacion', 'ocasion')
    search_fields = ('user__nombre_completo', 'ocasion')

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

admin.site.register(Reservacion, ReservacionAdmin)