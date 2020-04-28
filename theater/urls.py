from django.urls import path
from . import views

app_name='theater'

urlpatterns = [
    path('', views.movies_list, name="movies_list"),
]
