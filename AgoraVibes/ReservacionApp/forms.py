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
        super().__init__(*args, **kwargs)
        # <- todo aquí dentro
        if self.instance and self.instance.fecha_reservacion:
            self.initial['fecha_reservacion'] = self.instance.fecha_reservacion.strftime('%Y-%m-%d')

    def clean(self):
        cleaned_data = super().clean()
        personas = cleaned_data.get('cantidad_personas')
        mesas = cleaned_data.get('cantidad_mesas')
        fecha = cleaned_data.get('fecha_reservacion')

        if personas is not None and mesas is not None:
            if personas > 44:
                raise ValidationError("No se pueden reservar más de 44 personas.")
            if mesas > 11:
                raise ValidationError("No se pueden reservar más de 11 mesas.")

        if fecha is not None:
            hoy = timezone.now().date()
            if fecha < hoy:
                raise ValidationError("La fecha de reservación no puede ser anterior a hoy.")

        return cleaned_data