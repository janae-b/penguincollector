from django.shortcuts import render
from .models import Penguin

def home(request):
  return render(request, 'home.html')

def about(request):
  return render(request, 'about.html')

def penguins_index(request):
  penguins = Penguin.objects.all()
  return render(request, 'penguins/index.html', { 'penguins': penguins })

