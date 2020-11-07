from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import FormView
from .forms import VideoForm
from .models import ExperimentoGangorra
from django.utils import timezone


class Index(FormView):

    def get(self, request, *args, **kwargs):
        context = {
            'titulo': 'Gangorra',
        }
        return render(request, 'gangorra/index.html', context=context)


def video_upload(request):
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.created_date = timezone.now()
            print(post)
            post.save()

            print("form ok!")
            return redirect('gangorra:index')
    else:
        form = VideoForm()
    return render(request, 'gangorra/videos.html', {
        'form': form
    })


class ListaVideos(FormView):

    def get(self, request, *args, **kwargs):
        posts = ExperimentoGangorra.objects.filter(created_date__lte=timezone.now()).order_by('created_date')
        return render(request, 'gangorra/lista_experimentos.html',
                      {'posts': posts, 'titulo': 'Lista de experimentos'})


class VideosDetail(FormView):
    def get(self, request, pk, *args, **kwargs):
        post = get_object_or_404(ExperimentoGangorra, pk=pk)
        post.videoArquivo = "/media/" + post.videoArquivo.name
        #video = ExperimentoGangorra.objects.filter(experimento_id=post.experimento_id)
        return render(request, 'gangorra/experimentos_detail.html', {'post': post})
