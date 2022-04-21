from django.shortcuts import render
from django.http import HttpResponse
from extract_data import *
from . import forms


def index(request):
    return render(request, 'my_app/index.html')

def countries(request):
    names = extract_countires()
    names = sorted(names)
    my_dict = {'stam' : names}
    return render(request, 'my_app/countries.html', context = my_dict)

def languages(request):
    names = extract_languages()
    names = sorted(names)
    my_dict = {'stam' : names}
    return render(request, 'my_app/languages.html', context = my_dict)

def productions(request):
    names = extract_productions()
    my_dict = {'stam' : names}
    return render(request, 'my_app/productions.html', context = my_dict)

def actors(request):
    names = extract_actors()
    names = sorted(names)
    my_dict = {'stam' : names}
    return render(request, 'my_app/actors.html', context = my_dict)

def directors(request):
    names = extract_directors()
    names = sorted(names)
    my_dict = {'stam' : names}
    return render(request, 'my_app/directors.html', context = my_dict)

def form_view(request):
    form = forms.MovieForm()

    if request.method == 'POST':
        form = forms.MovieForm(request.POST)

        if form.is_valid():
            vec = create_vec(form.cleaned_data)
            return result(request, calc_result(vec))

    my_dict = {'form' : form}
    return render(request, 'my_app/form.html', context = my_dict)

def result(request, res):
    res = "{:.2f}".format(res)
    my_dict = {'result' : res}
    return render(request, 'my_app/result.html', context = my_dict)
