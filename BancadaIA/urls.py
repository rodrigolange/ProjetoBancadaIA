from django.urls import path

from . import views

# caminho para o index.html.
# irah procurar a funcao index no arquivo views.py
urlpatterns = [
    path('', views.index, name='index'),
    path('spotnano/', views.spotnano, name='spotnano'),
    path('spotnano/experimentos/lista/', views.spotnano_experimentos_lista, name='spotnano_experimentos_lista'),
    path('spotnano/experimentos/new/', views.spotnano_experimentos_new, name='spotnano_experimentos_new'),
    path('spotnano/experimentos/<int:pk>/detalhe/', views.spotnano_experimentos_detail, name='spotnano_experimentos_detail'),
    path('spotnano/experimentos/<int:pk>/edit/', views.spotnano_experimentos_edit, name='spotnano_experimentos_edit'),
]
