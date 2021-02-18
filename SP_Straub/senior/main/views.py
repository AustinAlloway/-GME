from typing import Dict
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect
from django.http import QueryDict
import json
from . import spotify as g

# Create your views here.


def home(request):
    context = {
        'Submitted': False,
        'GenreDict': {" ":" ",}
    }
    context2 = False
    return render(request, 'home.html', context)

def sample_sub(request):
    if request.method == 'POST':
        x = {
            'GenreDict' : g.get_total_genre_list(request.POST['sup']),
            'Submitted': True
        }
        print(x)
        return render(request, 'home.html', x)