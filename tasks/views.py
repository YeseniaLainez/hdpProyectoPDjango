import os
import chardet
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import Task
import csv
import requests
from django.shortcuts import render
from io import StringIO
from .forms import TaskForm
import zipfile
import io
import tempfile

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


@login_required
def tasks(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, 'home.html', {"home": tasks})

@login_required
def tasks_completed(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    return render(request, 'home.html', {"tasks": tasks})


@login_required
def create_task(request):
    if request.method == "GET":
        return render(request, 'create_task.html', {"form": TaskForm})
    else:
        try:
            form = TaskForm(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'create_task.html', {"form": TaskForm, "error": "Error creating task."})

#Se llama todos los navegadores para usuario
def home(request):
    return render(request, 'home.html')

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
    return render(request, 'publicaciones.html')

def paginas(request):
    return render(request, 'paginas.html')

def configuraciones(request):
    return render(request, 'configuraciones.html')


@login_required
def signout(request):
    logout(request)
    return redirect('home')

"""
def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {"form": AuthenticationForm})
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html', {"form": AuthenticationForm, "error": "Username or password is incorrect."})

        login(request, user)
        return redirect('home')
"""
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
def task_detail(request, task_id):
    if request.method == 'GET':
        task = get_object_or_404(Task, pk=task_id, user=request.user)
        form = TaskForm(instance=task)
        return render(request, 'task_detail.html', {'task': task, 'form': form})
    else:
        try:
            task = get_object_or_404(Task, pk=task_id, user=request.user)
            form = TaskForm(request.POST, instance=task)
            form.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'task_detail.html', {'task': task, 'form': form, 'error': 'Error updating task.'})

@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.datecompleted = timezone.now()
        task.save()
        return redirect('tasks')

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')
    



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
  
  
 
 
