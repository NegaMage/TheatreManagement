from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(movie)
admin.site.register(theatre)
admin.site.register(Profile)
admin.site.register(currentlyshowing)