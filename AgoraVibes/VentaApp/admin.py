from django.contrib import admin
from .models import Venta
from import_export.admin import ExportActionMixin
from AgoraVibes.ExportResource import CustomExportResource
from Detalle_VentaApp.models import DetalleVenta
from django.http import HttpResponse
from reportlab.pdfgen import canvas

def exportar_pdf(modeladmin, request, queryset):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="ventas.pdf"'
    pdf = canvas.Canvas(response)
    y = 800
    for venta in queryset:
        pdf.drawString(50, y, f"Venta ID: {venta.id}")
        y -= 20
        pdf.drawString(50, y, f"Usuario: {venta.usuario}")
        y -= 20
        pdf.drawString(50, y, f"Fecha: {venta.fecha}")
        y -= 30
        pdf.drawString(50, y, "Detalles:")
        y -= 20
        detalles = DetalleVenta.objects.filter(venta=venta)
        for d in detalles:
            texto = f"- {d.producto} | Cant: {d.cant_prod} | Total: {d.total}"
            pdf.drawString(60, y, texto)
            y -= 20
        y -= 10
        pdf.drawString(50, y, f"TOTAL VENTA: {venta.total}")
        y -= 40 
        if y < 100:
            pdf.showPage()
            y = 800

    pdf.save()
    return response

exportar_pdf.short_description = "Exportar a PDF"

class DetalleVentaInline(admin.TabularInline):
    model = DetalleVenta
    extra = 1
    
    autocomplete_fields = ['producto']

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        widget = formset.form.base_fields['producto'].widget
        widget.can_add_related = False
        widget.can_change_related = False
        widget.can_view_related = False
        return formset

class VentaResource (CustomExportResource):
    class Meta: 
        model = Venta
        fields = ('usuario', 'medio_pago', 'fecha')

class VentaAdmin(ExportActionMixin, admin.ModelAdmin):
    resource_class = VentaResource
    inlines = [DetalleVentaInline]
    actions = [exportar_pdf] 

    readonly_fields = ('usuario',)

    list_display = ('usuario', 'id', 'medio_pago', 'fecha', 'total')
    list_filter = ('usuario', 'id', 'medio_pago', 'fecha')
    search_fields = ('usuario__nombre_completo', 'id', 'usuario__numero_documento')
    search_help_text = "Nombre del usuario o por su número de documento, o ID de la venta."

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

admin.site.register(Venta, VentaAdmin)
