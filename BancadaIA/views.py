from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import ExperimentoSpotNano
from .forms import PostForm
from django.shortcuts import redirect
import time
from datetime import datetime
import os

#from django.http import HttpResponse


# corresponde ao definido no arquivo urls.py
def index(request):
    context = {
        'titulo': 'Bancada de Experimentos de IA',
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)


def spotnano(request):
    context = {
        'titulo': 'Spot Nano',
    }
    return render(request, 'spotnano/index.html', context=context)


def spotnano_experimentos_lista(request):
    posts = ExperimentoSpotNano.objects.filter(created_date__lte=timezone.now()).order_by('created_date')
    return render(request, 'spotnano/spotnano_experimentos_lista.html', {'posts': posts, 'titulo': 'Lista de experimentos com o Spot Nano'})


def spotnano_experimentos_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()

            #gera arquivo do experimento
            codigo = form.cleaned_data['codigo']
            codigo.replace('\r\r', '')
            print(codigo)
            filename = "teste.py" #datetime.now().strftime("%d-%m-%Y-%H-%M-%S") + ".py"
            f = open(".\\temp\\" + filename, "w", newline="\n") # newline="\n" evita o problema de fim de linha errado no arquivo
            f.write(codigo)
            f.close()

            # faz upload do experimento
            comandoUpload = "python webrepl/upload.py -p senha temp/teste.py 10.0.0.100:/experimentos/" #trocar para python3 no linux
            os.system(comandoUpload)
            print("terminei o upload")

            #executa experimento remotamente
            comandoExecutar = "python webrepl/executar.py"  # trocar para python3 no linux
            os.system(comandoExecutar)
            os.remove('temp/teste.py')

            return redirect('spotnano_experimentos_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'spotnano/spotnano_experimentos_edit.html', {'form': form})


def spotnano_experimentos_detail(request, pk):
    post = get_object_or_404(ExperimentoSpotNano, pk=pk)
    return render(request, 'spotnano/spotnano_experimentos_detail.html', {'post': post})


def spotnano_experimentos_edit(request, pk):
    post = get_object_or_404(ExperimentoSpotNano, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.created_date = timezone.now()
            post.save()
            return redirect('spotnano_experimentos_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'spotnano/spotnano_experimentos_edit.html', {'form': form})

