from django.urls import path
from . import views

# caminho para o index.html.
# irah procurar a funcao index no arquivo views.py
urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('spotnano/', views.SpotNano.as_view(), name='spotnano'),
    path('spotnano/experimentos/lista/', views.SpotNanoExperimentosLista.as_view(), name='spotnano_experimentos_lista'),
    path('spotnano/experimentos/new/', views.SpotNanoExperimentosNew.as_view(), name='spotnano_experimentos_new'),
    path('spotnano/experimentos/<int:pk>/detalhe/', views.SpotNanoExperimentosDetail.as_view(), name='spotnano_experimentos_detail'),
    path('spotnano/experimentos/<int:pk>/edit/', views.SpotNanoExperimentosEdit.as_view(), name='spotnano_experimentos_edit'),
    path('spotnano/experimentos/<task_id>/status/', views.SpotNanoExperimentosGetProgress, name='spotnano_experimentos_progress')
]
