import os
import chardet
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.utils import timezone
from django.contrib.auth.decorators import login_required

import csv
import requests
from django.shortcuts import render
from io import StringIO

import zipfile
import io
import tempfile
from .models import Container

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

def perfil(request):
    return render(request, 'perfil.html')

def exportar(request):
    return render(request, 'exportar.html')

#Se llama todos los navegadores para admin
def admin(request):
    return render(request, 'dashboard.html')
def dashadmin(request):
    return render(request, 'dashadmin.html')

def cuenta(request):
    return render(request, 'cuenta.html')

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
      url_grafico = ['https://datos.bancomundial.org/share/widget?end=2023&indicators=SL.UEM.TOTL.ZS&locations=SV&name_desc=false&start=2018&view=chart'
      'https://datos.bancomundial.org/share/widget?end=2022&indicators=SL.UEM.ADVN.FE.ZS&locations=SV&start=2018&view=chart'
      'https://datos.bancomundial.org/share/widget?end=2022&indicators=SL.UEM.TOTL.FE.ZS&locations=SV&start=2018&view=chart'
      'https://datos.bancomundial.org/share/widget?end=2022&indicators=SL.UEM.TOTL.MA.ZS&locations=SV&start=2018&view=chart'
      'https://datos.bancomundial.org/share/widget?end=2022&indicators=SL.UEM.ADVN.ZS&locations=SV&start=2018&view=chart'
      
      ]
       # Renderizar la plantilla con la URL del gráfico

      return render(request, 'info.html', {'url_grafico': url_grafico})
  
  
 
 
