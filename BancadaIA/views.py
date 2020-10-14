from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import ExperimentoSpotNano
from .forms import PostForm
from django.shortcuts import redirect
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
    return render(request, 'spotnano.html', context=context)

def listaexperimentos(request):
    posts = ExperimentoSpotNano.objects.filter(created_date__lte=timezone.now()).order_by('created_date')
    return render(request, 'listaexperimentos.html', {'posts': posts, 'titulo': 'Lista de experimentos com o Spot Nano'})


def post_detail(request, pk):
    post = get_object_or_404(ExperimentoSpotNano, pk=pk)
    return render(request, 'post_detail.html', {'post': post})


def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'post_edit.html', {'form': form})


def post_edit(request, pk):
    post = get_object_or_404(ExperimentoSpotNano, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.created_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'post_edit.html', {'form': form})

