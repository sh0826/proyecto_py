import re
from django import forms
from django.core.exceptions import ValidationError
from .models import Producto


class ProductoAdminForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={
                'pattern': r'[A-Za-zÁÉÍÓÚáéíóúÑñÜü\s]+',
                'title': 'Solo se permiten letras y espacios.',
                'maxlength': '20',
            }),
            'stock': forms.NumberInput(attrs={
                'min': 0,
                'max': 500,
                'step': 1,
                'inputmode': 'numeric',
            }),
            'precio_unitario': forms.NumberInput(attrs={
                'min': 0,
                'max': 500000,
                'step': 1,
                'inputmode': 'numeric',
            }),
        }

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre', '').strip()
        if not re.fullmatch(r'^[A-Za-zÁÉÍÓÚáéíóúÑñÜü\s]+$', nombre):
            raise ValidationError('El nombre solo puede contener letras y espacios.')
        return nombre

    def clean_stock(self):
        valor = self.cleaned_data.get('stock')
        if valor is None:
            raise ValidationError('El stock es obligatorio.')
        if valor < 0:
            raise ValidationError('El stock no puede ser negativo.')
        if valor > 500:
            raise ValidationError('El stock no puede superar 500.')
        return valor

    def clean_precio_unitario(self):
        valor = self.cleaned_data.get('precio_unitario')
        if valor is None:
            raise ValidationError('El precio unitario es obligatorio.')
        if valor < 0:
            raise ValidationError('El precio unitario no puede ser negativo.')
        if valor > 500000:
            raise ValidationError('El precio unitario no puede superar 500.000.')
        return valor
