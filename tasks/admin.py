"""from django.contrib import admin
from .models import Task
from .models import UsuarioComun

# Register your models here.
class TaskAdmin(admin.ModelAdmin):
  readonly_fields = ('created', )

<<<<<<< HEAD
admin.site.register(Task, TaskAdmin)"""
=======
admin.site.register(Task, TaskAdmin)
admin.site.register(UsuarioComun)
>>>>>>> e602bbf3aac9d058fdcc7daf36c3be423b4db902
