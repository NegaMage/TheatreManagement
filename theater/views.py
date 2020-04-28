from django.shortcuts import render
from .models import Show
# Create your views here.
def home(request):
    return render(request, "theater/home.html")

def movies_list(request):
    shows = Show.objects.all()

    args = {
        'shows': shows,
    }

    return render(request, 'theater/movies_list.html', args)
