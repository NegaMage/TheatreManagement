from django.shortcuts import render, HttpResponse, redirect
from .models import Show, Movie, Theatre
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.utils.timezone import datetime 
from django.contrib.auth.decorators import login_required
from . import forms


# Create your views here.
def home(request):
    return render(request, "theater/home.html")

def movies_list(request):
    # air_till >=datetime.date.now()
    
    shows = Show.objects.all()

    args = {
        'shows': shows,
    }

    return render(request, 'theater/movies_list.html', args)

def show_view(request, name, title):
    movie=Movie.objects.get(slug_title=title)
    theatre=Theatre.objects.get(slug_name=name)
    show=Show.objects.get(movie=movie,theatre=theatre)

    args = {
        'show': show,
    }

    return render(request, 'theater/show_view.html', args)

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('theater:movies_list')
    else:
        form = UserCreationForm()
    args = {
        'form':form,
    }
    
    return render(request, 'theater/signup_view.html', args)

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid() :
            user = form.get_user()
            login(request, user)
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect("theater:movies_list")

    form = AuthenticationForm()
    args = {
        'form':form,
    }
    return render(request, 'theater/login.html', args)

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('theater:movies_list')

@login_required(login_url='/theater/login')
def purchase(request):
    if request.method == 'POST':
        form = forms.MakePurchase(request.POST, request.FILES)
        if form.is_valid() :
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            return redirect('theater:movies_list')
    form = forms.MakePurchase()
    args = {
        'form':form,
    }
    return render(request, 'theater/purchase.html', args)