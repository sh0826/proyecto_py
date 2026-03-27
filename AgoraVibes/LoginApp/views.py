import string
import random
from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .models import Usuario
from .forms import RegistroForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from AgoraVibes import settings
from django.contrib.auth.hashers import make_password
from django.urls import reverse
from .models import Usuario, Recuperar

# Create your views here.


def registrar_usuario(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegistroForm()
    return render(request, 'registrar.html', {'form': form})

def iniciar_sesion(request):
    if request.method == 'POST':
        # AuthenticationForm por defecto usa el USERNAME_FIELD (documento)
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def cerrar_sesion(request):
    logout (request)
    return redirect ('/')

def recuperar(request):
    if request.method == 'POST':
        correo = request.POST.get('correo')

        user = Usuario.objects.filter(correo=correo).first()

        if user:
            caracteres = string.ascii_letters + string.digits
            codigo = ''.join(random.choices(caracteres, k=64))

            recup = Recuperar.objects.create(
                correo=user.correo,
                token=codigo
            )

            url_cc = f'http://localhost:8000/autenticar/cambiar_contraseña?c={user.correo}&t={codigo}'

            contexto = {'url_cc': url_cc, 'nom': user.nombre_completo}

            mensaje_html = render_to_string('correo_recup.html', contexto)

            email = EmailMessage(
                subject='Recuperación de Contraseña',
                body=mensaje_html,
                from_email=settings.EMAIL_HOST_USER,
                to=[user.correo]
            )

            email.content_subtype = 'html'
            email.send()

            msj = "La solicitud se ha procesado exitosamente"
            ok = 1
        else:
            msj = "El correo especificado no existe"
            ok = 0

        return render(request, 'recup.html', {'msj': msj, 'ok': ok})

    return render(request, 'recup.html')
    
    
def cambiar_contraseña(request):
    if request.method == 'POST':
        id_usr = request.POST.get('id')
        pw = request.POST.get('pass')
        pw2 = request.POST.get('pass2')
        user = Usuario.objects.get(numero_documento = id_usr)

        if not id_usr:
            messages.error(request, 'ID de usuario no recibido')
            return render(request, 'cambiar_pass.html')

        if pw != pw2:
            messages.error = 'La Contraseña y su confirmación no coinciden'
            return render(request, 'cambiar_pass.html', {'id_usr' : user.numero_documento})
        else:
            user = Usuario.objects.get(numero_documento = id_usr)
            user.password = make_password(pw, salt=None, hasher='default')
            user.save(update_fields=['password'])
            return redirect('/autenticar/login')
    else:
      cor = request.GET.get('c')
      tok = request.GET.get('t')
      recup = Recuperar.objects.filter(correo = cor, token = tok)
      user = Usuario.objects.get(correo = cor)
      if recup and user:
          recup.delete()                    
          return render(request, 'cambiar_pass.html', {'id_usr' : user.numero_documento})
      else:
          messages.error = "No se puede realizar el Cambio"
          return render(request, 'cambiar_pass.html')
      
        