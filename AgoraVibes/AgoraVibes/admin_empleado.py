from django.contrib.admin import AdminSite, ModelAdmin
from import_export.admin import ExportActionMixin
from AgoraVibes.ExportResource import CustomExportResource

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

class ReadOnlyModelAdmin(ExportActionMixin, ModelAdmin):
    resource_class = CustomExportResource
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
    search_help_text = "Puedes buscar por número de documento o nombre completo del usuario."

class DetalleVentaReadOnlyAdmin(ReadOnlyModelAdmin):
    list_display = ('producto', 'cant_prod')

class VentaReadOnlyAdmin(ReadOnlyModelAdmin):
    list_display = ('usuario', 'medio_pago', 'fecha')
    list_filter = ('usuario', 'medio_pago', 'fecha')
    search_fields = ('usuario__nombre_completo', 'usuario__numero_documento')
    search_help_text = "Nombre del usuario o por su número de documento."

class ReservacionReadOnlyAdmin(ReadOnlyModelAdmin):
    list_display = ('user', 'cantidad_personas', 'cantidad_mesas', 'fecha_reservacion', 'ocasion')
    search_fields = ('user__nombre_completo', 'ocasion')
    search_help_text = "Puedes buscar por nombre del usuario o por la ocasión de la reservación."

empleado_admin_site.register(DetalleVenta, DetalleVentaReadOnlyAdmin)
empleado_admin_site.register(Reservacion, ReservacionReadOnlyAdmin)
empleado_admin_site.register(Venta, VentaReadOnlyAdmin)
empleado_admin_site.register(Usuario, UsuarioReadOnlyAdmin)
