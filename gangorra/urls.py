from django.urls import path
from . import views



app_name = "gangorra"

urlpatterns = [
    path("", views.Index.as_view(), name="index"),
    path("video_upload", views.video_upload, name="video_upload"),
    path('experimentonovo', views.NovoExperimento.as_view(), name='experimentos_novo'),
    path('experimentos/lista/', views.ListaVideos.as_view(), name='experimentos_lista'),
    path('experimentos/<int:pk>/detalhe/', views.VideosDetail.as_view(), name='experimentos_detail'),
]
