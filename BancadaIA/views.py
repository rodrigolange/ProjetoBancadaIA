from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import ExperimentoSpotNano
from .forms import PostForm
from django.shortcuts import redirect
from django.views.generic.edit import FormView

from .tasks import enviarCodigoTask


#from django.http import HttpResponse


class Index(FormView):
    def get(self, request, *args, **kwargs):
        context = {
            'titulo': 'Bancada de Experimentos de IA',
        }
        return render(request, 'index.html', context=context)


class SpotNano(FormView):

    def get(self, request, *args, **kwargs):
        context = {
            'titulo': 'Spot Nano',
        }
        return render(request, 'spotnano/index.html', context=context)


class SpotNanoExperimentosLista(FormView):

    def get(self, request, *args, **kwargs):
        posts = ExperimentoSpotNano.objects.filter(created_date__lte=timezone.now()).order_by('created_date')
        return render(request, 'spotnano/spotnano_experimentos_lista.html',
                      {'posts': posts, 'titulo': 'Lista de experimentos com o Spot Nano'})


class SpotNanoExperimentosEdit(FormView):

    def get(self, request, pk, *args, **kwargs):
        post = get_object_or_404(ExperimentoSpotNano, pk=pk)
        form = PostForm(instance=post)
        return render(request, 'spotnano/spotnano_experimentos_edit.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.created_date = timezone.now()
            post.save()

            codigo = form.cleaned_data['codigo']
            codigo.replace('\r\r', '')
            enviarCodigoTask.delay('10.0.0.100', '8266', codigo)
            return redirect('spotnano_experimentos_detail', pk=post.pk)


class SpotNanoExperimentosNew(FormView):
    def get(self, request, *args, **kwargs):
        form = PostForm()
        return render(request, 'spotnano/spotnano_experimentos_edit.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()

            #gera arquivo do experimento
            codigo = form.cleaned_data['codigo']
            codigo.replace('\r\r', '')

            enviarCodigoTask.delay('10.0.0.100', '8266', codigo)

            return redirect('spotnano_experimentos_detail', pk=post.pk)


class SpotNanoExperimentosDetail(FormView):
    def get(self, request, pk, *args, **kwargs):
        post = get_object_or_404(ExperimentoSpotNano, pk=pk)
        return render(request, 'spotnano/spotnano_experimentos_detail.html', {'post': post})