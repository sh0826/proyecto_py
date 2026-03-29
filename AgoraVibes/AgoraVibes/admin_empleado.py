from django.contrib.admin import AdminSite, ModelAdmin

from Detalle_VentaApp.models import DetalleVenta
from ReservacionApp.models import Reservacion
from VentaApp.models import Venta
from LoginApp.models import Usuario

class EmpleadoAdminSite(AdminSite):
    site_header = 'Panel de Empleado'
    site_title = 'Administración - Empleados'
    index_title = 'Bienvenido al Panel de Empleado'

    def has_permission(self, request):
        return request.user.is_active and getattr(request.user, 'tipo', 0) == 2

empleado_admin_site = EmpleadoAdminSite(name='panel_empleado')

class ReadOnlyModelAdmin(ModelAdmin):
    def has_module_permission(self, request):
        return True

    def has_view_permission(self, request, obj=None):
        return True

    def has_add_permission(self, request):
        return False
    def has_change_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return False
    
class UsuarioReadOnlyAdmin(ReadOnlyModelAdmin):
    list_display = ('numero_documento', 'nombre_completo', 'correo', 'tipo', 'is_active')
    search_fields = ('numero_documento', 'nombre_completo')

class ReservacionReadOnlyAdmin(ReadOnlyModelAdmin):
    list_display = ('user', 'cantidad_personas', 'cantidad_mesas', 'fecha_reservacion', 'ocasion')
    search_fields = ('user__nombre_completo', 'ocasion')

empleado_admin_site.register(DetalleVenta, ReadOnlyModelAdmin)
empleado_admin_site.register(Reservacion, ReservacionReadOnlyAdmin)
empleado_admin_site.register(Venta, ReadOnlyModelAdmin)
empleado_admin_site.register(Usuario, UsuarioReadOnlyAdmin)
