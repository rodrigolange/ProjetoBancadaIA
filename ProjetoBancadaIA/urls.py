from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
]

# Projeto Bancada de Experimentos IA
urlpatterns += [
    path('BancadaIA/', include('BancadaIA.urls')),
    path('usuarios/', include('usuarios.urls')),
    path('gangorra/', include('gangorra.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
