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

    def clean(self): # esto se llama después de validar cada campo individualmente, aquí validamos en conjunto que todo tenga sentido y no halla contradicciones entre los campos
        cleaned_data = super().clean() # el cleaned_data es un diccionario con los datos limpios de cada campo, ya validados individualmente, aquí podemos acceder a ellos para hacer validaciones más complejas
        personas = cleaned_data.get('cantidad_personas')
        mesas = cleaned_data.get('cantidad_mesas')
        fecha = cleaned_data.get('fecha_reservacion')

        if personas is not None and mesas is not None: # el is not None es para asegurarnos que el campo no esté vacío, porque si el campo está vacío el cleaned_data tendrá un valor de None, y no podemos comparar None con un número, eso nos daría un error, entonces primero verificamos que no sea None antes de hacer las comparaciones es una buena práctica para evitar errores inesperados
            if personas > 44:
                raise ValidationError("No se pueden reservar más de 44 personas.")
            if mesas > 11:
                raise ValidationError("No se pueden reservar más de 11 mesas.") #el raise ValidationError es para lanzar un error de validación, esto hará que el formulario no se guarde y mostrará el mensaje de error al usuario, es importante lanzar un ValidationError dentro del método clean para que el formulario sepa que hubo un error de validación y no intente guardar los datos

        if fecha is not None:
            hoy = timezone.now().date()
            if fecha < hoy:
                raise ValidationError("La fecha de reservación no puede ser anterior a hoy.")

        return cleaned_data