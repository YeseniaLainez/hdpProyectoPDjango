
from pyexpat.errors import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
import csv
import requests
from django.shortcuts import render
from io import StringIO
from .forms import UserProfileForm
import zipfile
import io
import tempfile
<<<<<<< HEAD
from django.contrib import messages
=======
>>>>>>> c737b8e48b47968f44b7f8cee5450feb5cca0857
from .models import Container,UsuarioComun

# Create your views here.


def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {"form": UserCreationForm})
    else:

        if request.POST["password1"] == request.POST["password2"]:
            try:
                user = User.objects.create_user(
                    request.POST["username"], password=request.POST["password1"])
                user.save()
                login(request, user)
                return redirect('home')
            except IntegrityError:
                return render(request, 'signup.html', {"form": UserCreationForm, "error": "Username already exists."})

        return render(request, 'signup.html', {"form": UserCreationForm, "error": "Passwords did not match."})

#Se llama todos los navegadores para usuario
def home(request):
    containers = Container.objects.all()
    return render(request, 'home.html', {'containers': containers})

def info(request):
    return render(request, 'info.html')

@login_required
def perfil(request):
    usuario_comun = UsuarioComun.objects.filter(user=request.user).first()
    tiene_info = usuario_comun is not None

    form = UserProfileForm(instance=usuario_comun) if not tiene_info else None

    return render(request, 'perfil.html', {
        'usuario': usuario_comun,
        'tiene_info': tiene_info,
        'form': form
    })



def exportar(request):
    return render(request, 'exportar.html')

#Se llama todos los navegadores para admin
def admin(request):
    return render(request, 'dashboard.html')
def dashadmin(request):
    return render(request, 'dashadmin.html')

"""@login_required
def cuenta(request):
    # Verifica si el usuario actual es un superusuario
    if not request.user:
        return redirect('home')

    users = User.objects.all()
    usuarios_comunes = UsuarioComun.objects.all()
    usuarios_con_info = {usuario.user_id: usuario for usuario in usuarios_comunes}

    return render(request, 'cuenta.html', {
        'users': users,
        'usuarios_con_info': usuarios_con_info
    })"""
"""@login_required
def cuenta(request):
    if not request.user:
        return redirect('home')

    users = User.objects.all()
    usuarios_comunes = UsuarioComun.objects.all()
    usuarios_con_info = {usuario.user_id: usuario for usuario in usuarios_comunes}
    
    users_with_info = []
    for user in users:
        usuario = usuarios_con_info.get(user.id)
        if usuario:
            users_with_info.append({
                'username': user.username,
                'nombre': usuario.nombre,
                'edad': usuario.edad,
                'fecha_nacimiento': usuario.fecha_nacimiento,
                'telefono': usuario.telefono,
                'direccion': usuario.direccion,
            })
        else:
            users_with_info.append({
                'username': user.username,
                'nombre': 'No registrado',
                'edad': 'No registrado',
                'fecha_nacimiento': 'No registrado',
                'telefono': 'No registrado',
                'direccion': 'No registrado',
            })

    return render(request, 'cuenta.html', {
        'users_with_info': users_with_info,
    })"""

@login_required
def cuenta(request):
    if not request.user:
        return redirect('home')

    users = User.objects.all()
    usuarios_comunes = UsuarioComun.objects.all()
    usuarios_con_info = {usuario.user_id: usuario for usuario in usuarios_comunes}
    
    users_with_info = []
    for user in users:
        usuario = usuarios_con_info.get(user.id)
        if usuario:
            users_with_info.append({
                'user_id': user.id,
                'username': user.username,
                'nombre': usuario.nombre,
                'edad': usuario.edad,
                'fecha_nacimiento': usuario.fecha_nacimiento,
                'telefono': usuario.telefono,
                'direccion': usuario.direccion,
            })
        else:
            users_with_info.append({
                'user_id': user.id,
                'username': user.username,
                'nombre': 'No registrado',
                'edad': 'No registrado',
                'fecha_nacimiento': 'No registrado',
                'telefono': 'No registrado',
                'direccion': 'No registrado',
            })

    return render(request, 'cuenta.html', {
        'users_with_info': users_with_info,
    })


def publicaciones(request):
    containers = Container.objects.all()
    return render(request, 'publicaciones.html',{'containers': containers})

def paginas(request):
    return render(request, 'paginas.html')

def configuraciones(request):
    return render(request, 'configuraciones.html')


@login_required
def signout(request):
    logout(request)
    return redirect('home')

def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {"form": AuthenticationForm()})
    else:
        username = request.POST['username']
        password = request.POST['password']
        
        if username == 'mario' and password == '231':
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('admin')
            else:
                return render(request, 'signin.html', {"form": AuthenticationForm(), "error": "Username or password is incorrect."})
        else:
            user = authenticate(request, username=username, password=password)
            if user is None:
                return render(request, 'signin.html', {"form": AuthenticationForm(), "error": "Username or password is incorrect."})
            login(request, user)
            return redirect('home')

@login_required
def add_container(request):
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        image = request.FILES.get('image')
        Container.objects.create(title=title, content=content,image=image, user=request.user)
    return redirect('publicaciones')

@login_required
def delete_container(request, container_id):
    container = get_object_or_404(Container, id=container_id)
    if request.user:
        container.delete()
    return redirect('publicaciones')

@login_required
def update_container(request, container_id):
    container = get_object_or_404(Container, id=container_id)
    if request.method == 'POST':
        container.title = request.POST['title']
        container.content = request.POST['content']
        container.image = request.FILES.get('image', container.image)
        container.save()
    return redirect('publicaciones')

def graficoDesempleo_view(request):
       # Obtener la URL de compartir del gráfico (reemplaza con la URL real)
      url_grafico = ['https://datos.bancomundial.org/share/widget?end=2023&indicators=SL.UEM.ADVN.MA.ZS&locations=SV&most_recent_value_desc=false&start=2018&view=chart'
      'https://datos.bancomundial.org/share/widget?end=2022&indicators=SL.UEM.ADVN.FE.ZS&locations=SV&start=2018&view=chart'
      'https://datos.bancomundial.org/share/widget?end=2023&indicators=SL.UEM.TOTL.FE.ZS&locations=SV&most_recent_value_desc=false&start=2018&view=chart'
      'https://datos.bancomundial.org/share/widget?end=2023&indicators=SL.UEM.TOTL.MA.ZS&locations=SV&most_recent_value_desc=false&start=2018&view=chart'
      'https://datos.bancomundial.org/share/widget?end=2023&indicators=SL.UEM.TOTL.ZS&locations=SV&most_recent_value_desc=false&start=2018&view=chart'
      'https://datos.bancomundial.org/share/widget?end=2023&indicators=SL.UEM.ADVN.ZS&locations=SV&most_recent_value_desc=false&start=2018&view=chart'
      
      ]
       # Renderizar la plantilla con la URL del gráfico

      return render(request, 'info.html', {'url_grafico': url_grafico})
  
  
def graficoPIB_view(request):
       # Obtener la URL de compartir del gráfico (reemplaza con la URL real)
      url_graficos = ['https://datos.bancomundial.org/share/widget?end=2022&indicators=NY.GDP.MKTP.CD&locations=SV&start=2018'
      'https://datos.bancomundial.org/share/widget?end=2022&indicators=NY.GDP.MKTP.KD.ZG&locations=SV&start=2018'
      ]
       # Renderizar la plantilla con la URL del gráfico

      return render(request, 'info.html', {'url_graficos': url_graficos})
  
<<<<<<< HEAD
from django.shortcuts import get_object_or_404

"""@require_http_methods(["POST", "GET"])
=======

@require_http_methods(["POST", "GET"])
>>>>>>> c737b8e48b47968f44b7f8cee5450feb5cca0857
def guardar_usuario(request):
    if request.method == 'POST':
        usuario_django = request.user

        # Verifica si el usuario ya tiene un UsuarioComun asociado
        usuario_comun_existente = UsuarioComun.objects.filter(user=usuario_django).first()

        if usuario_comun_existente:
            # Si existe, actualiza los detalles del usuario
            usuario_comun_existente.nombre = request.POST['nombre']
            usuario_comun_existente.edad = request.POST['edad']
            usuario_comun_existente.fecha_nacimiento = request.POST['fecha_nacimiento']
            usuario_comun_existente.telefono = request.POST['telefono']
            usuario_comun_existente.direccion = request.POST['direccion']
            usuario_comun_existente.save()
        else:
            # Si no existe, crea uno nuevo
            nombre = request.POST['nombre']
            edad = request.POST['edad']
            fecha_nacimiento = request.POST['fecha_nacimiento']
            telefono = request.POST['telefono']
            direccion = request.POST['direccion']

            usuario_comun = UsuarioComun(
                user=usuario_django,
                nombre=nombre,
                edad=edad,
                fecha_nacimiento=fecha_nacimiento,
                telefono=telefono,
                direccion=direccion
            )
            usuario_comun.save()

        # Redirige a alguna URL después de guardar
        return redirect('home')

    return render(request, 'perfil.html')"""
from django.shortcuts import get_object_or_404

@login_required
@require_http_methods(["POST", "GET"])
def guardar_usuario(request):
    usuario_django = request.user
    usuario_comun_existente = UsuarioComun.objects.filter(user=usuario_django).first()
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=usuario_comun_existente)
        if form.is_valid():
            usuario_comun = form.save(commit=False)
            usuario_comun.user = usuario_django
            usuario_comun.save()
            return redirect('home')
    else:
        form = UserProfileForm(instance=usuario_comun_existente)

    return render(request, 'perfil.html', {
        'form': form,
        'usuario': usuario_comun_existente,
        'tiene_info': usuario_comun_existente is not None
    })
#Para editar usuario desde admin
@login_required
def edit_user(request, user_id):
    user_instance = get_object_or_404(User, id=user_id)
    user_profile_instance = get_object_or_404(UsuarioComun, user=user_instance)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user_profile_instance)
        password_form = PasswordChangeForm(user_instance, request.POST)
        if form.is_valid() and password_form.is_valid():
            form.save()
            user = password_form.save()
            update_session_auth_hash(request, user)  # Mantener al usuario logueado después de cambiar la contraseña
            return redirect('cuenta')
        else:
            # Depuración: imprime errores en la consola
            print(form.errors)
            print(password_form.errors)
    else:
        form = UserProfileForm(instance=user_profile_instance)
        password_form = PasswordChangeForm(user_instance)
    return render(request, 'edit_user.html', {
        'form': form,
        'password_form': password_form,
        'user_instance': user_instance
    })
#para eliminar usuario desde admin
@login_required
def delete_user(request, user_id):
    user_instance = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        user_instance.delete()
        return redirect('cuenta')
    
    return render(request, 'confirm_delete.html', {
        'user_instance': user_instance
    })
    
"""def perfil_usuario(request):
    try:
        usuario = UsuarioComun.objects.get(user=request.user)  # Asumiendo que cada usuario tiene un solo perfil
        tiene_info = True
    except UsuarioComun.DoesNotExist:
        usuario = None
        tiene_info = False

<<<<<<< HEAD
    return render(request, 'perfil.html', {'usuario': usuario, 'tiene_info': tiene_info})"""

"""def profile(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = UserProfileForm(instance=user_profile)
    return render(request, 'perfil.html', {'form': form})
    

def cuenta(request):
    if not request.user:
        return redirect('home')
    users = UsuarioComun.objects.all()
    return render(request, 'cuenta.html', {'users': users})"""
"""
@login_required
def user_detail(request, user_id):
    if not request.user:
        return redirect('profile')
    user = get_object_or_404(CustomUser, id=user_id)
    user_profile = UserProfile.objects.filter(user=user).first()
    return render(request, 'user_detail.html', {'user': user, 'profile': user_profile})"""
=======
    return render(request, 'perfil.html', {'usuario': usuario, 'tiene_info': tiene_info})
 
>>>>>>> c737b8e48b47968f44b7f8cee5450feb5cca0857
