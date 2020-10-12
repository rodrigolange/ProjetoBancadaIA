from django.shortcuts import render
#from django.http import HttpResponse
from .forms import PostForm


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


def post_new(request):
    form = PostForm()
    return render(request, 'experimentospotnano.html', {'form': form})

