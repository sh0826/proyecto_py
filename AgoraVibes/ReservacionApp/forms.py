from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import reservacion

class ReservacionForm(forms.ModelForm):
    class Meta:
        model = reservacion
        fields = ['cantidad_personas', 'cantidad_mesas', 'fecha_reservacion', 'ocasion']

        widgets = {
            'cantidad_personas': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Cantidad de personas',
                'min': 1,       # mínimo 1 persona
                'max': 44       # máximo 44 personas
            }),
            'cantidad_mesas': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Cantidad de mesas',
                'min': 1,       # mínimo 1 mesa
                'max': 11       # máximo 11 mesas
            }),
            'fecha_reservacion': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'min': timezone.now().date().strftime('%Y-%m-%d')
            }),
            'ocasion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Cumpleaños'
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        personas = cleaned_data.get('cantidad_personas')
        mesas = cleaned_data.get('cantidad_mesas')
        fecha = cleaned_data.get('fecha_reservacion')

        # Validar que personas > mesas
        if personas is not None and mesas is not None:
            if personas <= mesas:
                raise ValidationError("La cantidad de personas debe ser mayor que la cantidad de mesas.")

            if personas > 44:
                raise ValidationError("No se pueden reservar más de 44 personas.")

            if mesas > 11:
                raise ValidationError("No se pueden reservar más de 11 mesas.")

        # Validar que la fecha no sea pasada
        if fecha is not None:
            hoy = timezone.now().date()
            if fecha < hoy:
                raise ValidationError("La fecha de reservación no puede ser anterior a hoy.")

        return cleaned_data