from django.db import models
from django.contrib.auth.models import User

# Create your models here.

"""class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=1000)
    created = models.DateTimeField(auto_now_add=True)
    datecompleted = models.DateTimeField(null=True, blank=True)
    important = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)"""

class Container(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class UsuarioComun(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=255, blank=True, null=True)
    edad = models.PositiveIntegerField(blank=True, null=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title + ' - ' + self.user.username
    
class UsuarioComun(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=255, blank=True, null=True)
    edad = models.PositiveIntegerField(blank=True, null=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)
