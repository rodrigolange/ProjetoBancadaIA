from django.urls import path

from . import views

# caminho para o index.html.
# irah procurar a funcao index no arquivo views.py
urlpatterns = [
    path('', views.index, name='index'),
    path('spotnano/', views.spotnano, name='spotnano'),
    #path('experimentospotnano/', views.experimentospotnano, name='experimentospotnano'),
]
