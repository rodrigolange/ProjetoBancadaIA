from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import FormView
from .forms import FormVideo, FormExperimento
from .models import ExperimentoGangorra
from django.utils import timezone
from .tasks import enviarCodigoTask


class Index(FormView):

    def get(self, request, *args, **kwargs):
        context = {
            'titulo': 'Gangorra Controle',
        }
        return render(request, 'gangorra/index.html', context=context)


class NovoExperimento(FormView):
    def get(self, request, *args, **kwargs):
        form = FormExperimento()
        context = {
            'titulo': 'Gangorra Controle',
            'form': form,
        }
        return render(request, 'gangorra/experimentos_novo.html', context=context)

    def post(self, request, *args, **kwargs):
        form = FormExperimento(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.created_date = timezone.now()

            #gera arquivo do experimento
            codigo = "import PID\npid=PID.PID()\npid.executa("
            codigo = codigo + "referencia=" + post.modelo_referencia + ", "
            codigo = codigo + "kp=" + post.modelo_kp + ", "
            codigo = codigo + "ki=" + post.modelo_ki + ", "
            codigo = codigo + "kd=" + post.modelo_kd + ", "
            codigo = codigo + "repeticoes=" + post.modelo_repeticoes
            codigo = codigo + ")\n"

            taskID = enviarCodigoTask.delay('10.0.0.210', codigo)

            #print(f'ID da task:{taskID}')

            #return redirect('spotnano_experimentos_detail', pk=post.pk)
            #return redirect('BancadaIA:spotnano_experimentos_progress', taskID)

            return redirect('gangorra:experimentos_lista')


def video_upload(request):
    if request.method == 'POST':
        form = FormVideo(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            print(request.user)
            post.created_date = timezone.now()
            post.save()
            return redirect('gangorra:index')
    else:
        form = FormVideo()
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
