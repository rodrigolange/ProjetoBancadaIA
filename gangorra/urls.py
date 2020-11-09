from django.urls import path
from . import views

app_name = "gangorra"

urlpatterns = [
    path("", views.Index.as_view(), name="index"),
    path('experimentonovo', views.ExperimentoNovo.as_view(), name='experimentos_novo'),
    path('experimentos/<task_id>/status/', views.ExperimentoGetProgress, name='experimentos_progress'),
    path('experimentos/<task_id>/statusframe/', views.ExperimentoGetProgressFrame.as_view(), name='experimentos_progressframe'),
    path('experimentos/lista/', views.VideosLista.as_view(), name='experimentos_lista'),
    path('experimentos/<int:pk>/detalhe/', views.VideosDetail.as_view(), name='experimentos_detail'),
]
