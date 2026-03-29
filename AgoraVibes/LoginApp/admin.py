from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.forms import TextInput, Textarea
from django import forms
from .models import Usuario
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.models import Group


class UsuarioCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirmar contraseña', widget=forms.PasswordInput)
    tipo = forms.ChoiceField(
        choices= [(1, 'Administrador'), (2, 'Empleado'), (3, 'Cliente')],
        label="Tipo"
    )

    class Meta:
        model = Usuario
        fields = ('numero_documento', 'nombre_completo', 'correo', 'tipo')


    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Las contraseñas no coinciden")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class UsuarioChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(label=("Contraseña"))

    class Meta:
        model = Usuario
        fields = ('numero_documento', 'nombre_completo', 'correo', 'tipo', 'password', 'is_active', 'is_staff', 'is_superuser')

class UsuarioAdmin(BaseUserAdmin):
    form = UsuarioChangeForm
    add_form = UsuarioCreationForm

    list_display = ('numero_documento', 'nombre_completo', 'correo', 'tipo', 'is_staff', 'is_active')
    list_filter = ('tipo', 'is_active')

    fieldsets = (
        (None, {'fields': ('numero_documento', 'password')}),
        ('Información personal', {'fields': ('nombre_completo', 'correo', 'tipo')}),
        ('Permisos', {'fields': ('is_staff', 'is_active', 'is_superuser')}),
        ('Fechas importantes', {'fields': ('last_login',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('numero_documento', 'nombre_completo', 'correo', 'tipo', 'password1', 'password2'),
        }),
    )

    search_fields = ('numero_documento', 'nombre_completo', 'correo')
    ordering = ('numero_documento',)
    filter_horizontal = ()

admin.site.register(Usuario, UsuarioAdmin)
admin.site.unregister(Group)

# urls.py
admin.site.site_header = "AgoraVibes"
admin.site.site_title = "Portal de AgoraVibes"
admin.site.index_title = "Panel de Administración"

