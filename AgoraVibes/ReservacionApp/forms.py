from email import errors

from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Reservacion

class ReservacionForm(forms.ModelForm):
    class Meta:
        model = Reservacion
        fields = ['cantidad_personas', 'cantidad_mesas', 'fecha_reservacion', 'ocasion']

        widgets = {
            'cantidad_personas': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Cantidad de personas',
                'min': 1,
                'max': 44
            }),
            'cantidad_mesas': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Cantidad de mesas',
                'min': 1,
                'max': 11
            }),
            'fecha_reservacion': forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'type': 'date',
                    'min': timezone.now().date().strftime('%Y-%m-%d')
                },
                format='%Y-%m-%d'
            ),
            'ocasion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Cumpleaños'
            }),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user',None)
        super().__init__(*args, **kwargs)
        # <- todo aquí dentro
        if self.instance and self.instance.fecha_reservacion:
            self.initial['fecha_reservacion'] = self.instance.fecha_reservacion.strftime('%Y-%m-%d')

    def clean(self):
    
        cleaned_data = super().clean()
        personas = cleaned_data.get('cantidad_personas')
        mesas = cleaned_data.get('cantidad_mesas')
        fecha = cleaned_data.get('fecha_reservacion')
        user = self.user

        errors = {}

        print("Ejecutando validación clean...")  # <--- Para verificar que se llame
    
    # El resto de tu código aquí...
    
        if errors:
            print("Errores encontrados:", errors)  # <--- Para ver qué errores detecta
            raise ValidationError(errors)

        if personas is not None:
            if personas > 44:
                errors['cantidad_personas'] = "No se pueden reservar más de 44 personas."

        if mesas is not None:
            if mesas > 11:
                errors['cantidad_mesas'] = "No se pueden reservar más de 11 mesas."

        if fecha is not None:
            hoy = timezone.now().date()
        if fecha < hoy:
            errors['fecha_reservacion'] = "La fecha de reservación no puede ser anterior a hoy."

        reservas_usuario = Reservacion.objects.none()

        if fecha and mesas and user and personas:
            reservas_usuario = Reservacion.objects.filter(
            fecha_reservacion=fecha,
            user=user
        )

            total_personas = sum(r.cantidad_personas for r in reservas_usuario)
            total_mesas = sum(r.cantidad_mesas for r in reservas_usuario)

        if total_personas + personas > 44:
            errors['cantidad_personas'] = (
                f"No puedes reservar más personas para este día. Ya hay {total_personas} personas reservadas."
            )

        if total_mesas + mesas > 11:
            errors['cantidad_mesas'] = (
                f"No puedes reservar más mesas para este día. Ya hay {total_mesas} mesas reservadas."
            )

        if errors:
            raise ValidationError(errors)

        return cleaned_data