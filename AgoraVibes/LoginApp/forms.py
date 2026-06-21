import re
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario

class RegistroForm(forms.ModelForm):

    password = forms.CharField(
        label="Contraseña",
        help_text="La contraseña debe tener mínimo 8 caracteres, una mayúscula, una minúscula, un número y un carácter especial.",
        widget=forms.PasswordInput)
    
    confirm_password = forms.CharField(
        label="Confirmar Contraseña",
        help_text="Ingrese la misma contraseña para confirmarla.",
        widget=forms.PasswordInput)
    
    class Meta:
        model = Usuario
        fields = ['numero_documento', 'nombre_completo', 'correo', 'password']

    # Sobrescribir el método save para cifrar la contraseña antes de guardar el usuario
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"]) # Cifrado de seguridad
        if commit:
            user.save()
        return user
    
    # Validación para asegurar que la contraseña cumpla con los requisitos de seguridad
    def clean_password(self):
        password = self.cleaned_data.get("password")

        if len(password) < 8:
            raise forms.ValidationError("La contraseña debe tener al menos 8 caracteres.")
        
        if not re.search(r'[A-Z]', password):
            raise forms.ValidationError("La contraseña debe contener al menos una letra mayúscula.")
        
        if not re.search(r'[a-z]', password):
            raise forms.ValidationError("La contraseña debe contener al menos una letra minúscula.")
        
        if not re.search(r'[0-9]', password):
            raise forms.ValidationError("La contraseña debe contener al menos un número.")
        
        if not re.search(r'[!@#$%^&*(),.?":{}|<>_]', password):
            raise forms.ValidationError("La contraseña debe contener al menos un carácter especial.")
        
        return password
    
    # Validación para asegurar que las contraseñas coincidan
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Las contraseñas no coinciden.")
        
        return cleaned_data