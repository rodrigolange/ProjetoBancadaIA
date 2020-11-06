from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
]

# Projeto Bancada de Experimentos IA
urlpatterns += [
    path('BancadaIA/', include('BancadaIA.urls')),
    path('usuarios/', include('usuarios.urls')),
]

