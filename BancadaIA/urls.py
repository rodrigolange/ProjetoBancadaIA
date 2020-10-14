from django.urls import path

from . import views

# caminho para o index.html.
# irah procurar a funcao index no arquivo views.py
urlpatterns = [
    path('', views.index, name='index'),
    path('spotnano/', views.spotnano, name='spotnano'),
    path('listaexperimentos/', views.listaexperimentos, name='listaexperimentos'),
    path('post/new/', views.post_new, name='post_new'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
]
