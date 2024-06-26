"""
URL configuration for hdpProyectoPDjango project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from tasks import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', views.home, name='home'),
    path('info/', views.info, name='info'),
    path('perfil/', views.guardar_usuario, name='guardar_usuario'),
    path('exportar/', views.exportar, name='exportar'),
    #path('admin/', admin.site.urls),
    path('adminD/', views.admin, name='admin'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.signout, name='logout'),
    path('', views.signin, name='signin'),
    path('dashadmin/', views.dashadmin, name='dashadmin'),
    path('cuenta/', views.cuenta, name='cuenta'),
    path('edit_user/<int:user_id>/', views.edit_user, name='edit_user'),
    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('publicaciones/', views.publicaciones, name='publicaciones'),
    path('paginas/', views.paginas, name='paginas'),
    path('configuraciones/', views.configuraciones, name='configuraciones'),
    path('info/', views.graficoDesempleo_view, name='info'),
    path('publicaciones/add/', views.add_container, name='add_container'),
    path('publicaciones/delete/<int:container_id>/', views.delete_container, name='delete_container'),
    path('publicaciones/update/<int:container_id>/', views.update_container, name='update_container'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)