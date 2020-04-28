from django.shortcuts import render, redirect, HttpResponse



def home(request):
    return render(request,'dbms/home.html')

def about(request):
    return render(request, 'dbms/about.html')