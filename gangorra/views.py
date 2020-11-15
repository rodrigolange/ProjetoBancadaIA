from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import FormView
from django.views.decorators.clickjacking import xframe_options_exempt
from .forms import FormVideo, FormExperimento
from .models import ExperimentoGangorra
from django.utils import timezone
from .tasks import enviarCodigoTask
from celery.result import AsyncResult
from datetime import datetime

class Index(FormView):

    def get(self, request, *args, **kwargs):
        context = {
            'titulo': 'Gangorra Controle',
        }
        return render(request, 'gangorra/index.html', context=context)


class ExperimentoNovo(FormView):
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

            filename = "exp" + datetime.now().strftime("%d%m%Y%H%M%S")

            #gera arquivo do experimento
            codigo = "import PID\npid=PID.PID()\npid.executa("
            codigo = codigo + "referencia=" + post.modelo_referencia + ", "
            codigo = codigo + "kp=" + post.modelo_kp + ", "
            codigo = codigo + "ki=" + post.modelo_ki + ", "
            codigo = codigo + "kd=" + post.modelo_kd + ", "
            codigo = codigo + "repeticoes=" + post.modelo_repeticoes + ", "
            codigo = codigo + "dfile='" + filename + ".csv'"
            codigo = codigo + ")\n"

            taskID = enviarCodigoTask.delay('10.0.0.210',
                                            codigo=codigo,
                                            filename=filename,
                                            autor="lange", #=post.author)
                                            kp=post.modelo_kp,
                                            ki=post.modelo_ki,
                                            kd=post.modelo_kd,
                                            ref=post.modelo_referencia,
                                            rep=post.modelo_repeticoes)

            return redirect('gangorra:experimentos_progress', taskID)


def ExperimentoGetProgress(request, task_id):

    response_data = {
        'taskID': task_id,
        'title': 'Gangorra Status',
    }
    return render(request, 'gangorra/experimentos_statusbase.html', response_data)


#@xframe_options_exempt
class ExperimentoGetProgressFrame(FormView):
    @xframe_options_exempt
    def get(self, request, task_id, *args, **kwargs):
        result = AsyncResult(task_id)
        percent = 0

        if result.status == 'PROGRESS':
            percent = result.info.get('percent')
        elif result.status == 'PENDING':
            percent = 0
        else:
            percent = 100

        response_data = {
            'percent': percent,
        }
        return render(request, 'gangorra/experimentos_statusFrame.html', response_data)


class ExperimentoDetalhe(FormView):
    def get(self, request, pk, *args, **kwargs):
        post = get_object_or_404(ExperimentoGangorra, pk=pk)

        print(post.videoArquivo.name)

        post.videoArquivo = "/media/gangorra/videos/" + post.videoArquivo.name
        post.csvArquivo = "/media/gangorra/csv/" + post.csvArquivo.name
        post.graficoArquivo = "/media/gangorra/graficos/" + post.graficoArquivo.name
        return render(request, 'gangorra/experimentos_detail.html', {'post': post})

#- videos -#

class VideosLista(FormView):

    def get(self, request, *args, **kwargs):
        posts = ExperimentoGangorra.objects.filter(created_date__lte=timezone.now()).order_by('created_date')
        return render(request, 'gangorra/lista_experimentos.html',
                      {'posts': posts, 'titulo': 'Lista de experimentos'})




