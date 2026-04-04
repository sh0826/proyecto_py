from django.contrib.admin import AdminSite, ModelAdmin
from django.contrib import admin
from import_export.admin import ExportActionMixin
from AgoraVibes.ExportResource import CustomExportResource
from Detalle_VentaApp.models import DetalleVenta
from ReservacionApp.models import Reservacion
from django.utils.html import mark_safe
from VentaApp.models import Venta
from LoginApp.models import Usuario
from EventoApp.models import Evento
from ProductoApp.models import Producto

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
    
    def has_export_permission(self, request):
        return False
    
class UsuarioReadOnlyAdmin(ReadOnlyModelAdmin):
    list_display = ('numero_documento', 'nombre_completo', 'correo', 'tipo', 'is_active')
    search_fields = ('numero_documento', 'nombre_completo')
    search_help_text = "Puedes buscar por número de documento o nombre completo del usuario."

class DetalleVentaReadOnlyAdmin(ReadOnlyModelAdmin):
    list_display = ('producto', 'venta', 'cant_prod', 'total_mostrado')
    def total_mostrado(self, obj):
        return obj.total
    total_mostrado.short_description = 'Total'
    
    def get_changeform_initial_data(self, request):
        initial = super().get_changeform_initial_data(request) 
        venta_id = request.GET.get('venta')
        if venta_id:    
            initial['venta']= venta_id
        return initial

class DetalleVentaInline(admin.TabularInline):
    model = DetalleVenta
    extra = 0
    readonly_fields = ('producto', 'cant_prod', 'total_item')
    fields = ('producto', 'cant_prod', 'total_item')
    
    def total_item(self, obj):
        return obj.total
    total_item.short_description = 'Total'

    def has_view_permission(self, request, obj=None):
        return True
    def has_add_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return False
    def has_change_permission(self, request, obj=None):
        return False
    
class VentaReadOnlyAdmin(ReadOnlyModelAdmin):
    list_display = ('usuario', 'id', 'medio_pago', 'fecha', 'total')
    list_filter = ('usuario', 'medio_pago', 'fecha')
    inlines = [DetalleVentaInline]
    search_fields = ('usuario__nombre_completo', 'id', 'usuario__numero_documento')
    search_help_text = "Nombre del usuario o por su número de documento, o ID de la venta."
    readonly_fields = ('usuario', 'total')
    
    def total(self, obj):
        return obj.total
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)

        class FormWithUser(form):
            def __init__(self2, *args, **kw):
                super().__init__(*args, **kw)
                if not obj:  
                    self2.instance.usuario = request.user
        return FormWithUser

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.usuario = request.user
        super().save_model(request, obj, form, change)


class ProductoReadOnlyAdmin(ReadOnlyModelAdmin):    
    list_display = (
        'nombre',
        'tipo',
        'cantidad_MD',
        'unidad_MD',
        'stock',
        'precio_unitario',
        'mostrar_imagen'
    )
    list_filter = (
        'tipo',
        'unidad_MD',
        'cantidad_MD',
        'precio_unitario',
    )
    search_fields = (        
        'nombre',
        'stock',
        'cantidad_MD',
        'precio_unitario',)
    search_help_text = "Nombre del producto, stock, cantidad de medida o precio unitario."
    
    readonly_fields = ('mostrar_imagen',)

    def mostrar_imagen(self, obj):
        if obj.imagen:
            return mark_safe(f'<img src="{obj.imagen.url}" width="100" height="100" style="object-fit: cover; border-radius: 5px;" />')
        return "Sin imagen"
    mostrar_imagen.short_description = 'Imagen'


class ReservacionReadOnlyAdmin(ReadOnlyModelAdmin):
    list_display = ('user', 'cantidad_personas', 'cantidad_mesas', 'fecha_reservacion', 'ocasion')
    search_fields = ('user__nombre_completo', 'ocasion')
    search_help_text = "Puedes buscar por nombre del usuario o por la ocasión de la reservación."

class EventoReadOnlyAdmin(ReadOnlyModelAdmin):
    list_display = ('nombre','capacidad_maxima', 'descripcion','fecha','hora_inicio','precio_boleta')
    search_fields = ('nombre', 'fecha', 'precio_boleta', 'hora_inicio')
    search_help_text = "Puedes buscar por el nombre del evento, precio y hora de inicio"

empleado_admin_site.register(Evento, EventoReadOnlyAdmin)
empleado_admin_site.register(DetalleVenta, DetalleVentaReadOnlyAdmin)
empleado_admin_site.register(Reservacion, ReservacionReadOnlyAdmin)
empleado_admin_site.register(Venta, VentaReadOnlyAdmin)
empleado_admin_site.register(Usuario, UsuarioReadOnlyAdmin)
empleado_admin_site.register(Producto, ProductoReadOnlyAdmin)
