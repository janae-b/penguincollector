from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .forms import FeedingForm
import uuid
import boto3
from .models import Penguin, Toy, Photo

S3_BASE_URL = 'https://s3.us-east-2.amazonaws.com/'
BUCKET = 'penguincollectorjb'


def home(request):
  return render(request, 'home.html')

def about(request):
  return render(request, 'about.html')

def penguins_index(request):
  penguins = Penguin.objects.all()
  return render(request, 'penguins/index.html', { 'penguins': penguins })

def penguins_detail(request, penguin_id):
  penguin = Penguin.objects.get(id=penguin_id)
  toys_penguin_doesnt_have = Toy.objects.exclude(id__in = penguin.toys.all().values_list('id'))
  feeding_form = FeedingForm()
  return render(request, 'penguins/detail.html', {
    'penguin': penguin, 'feeding_form': feeding_form,
    # Add the toys to be displayed
    'toys': toys_penguin_doesnt_have
  })

def add_feeding(request, penguin_id):
  form = FeedingForm(request.POST)
  if form.is_valid():
    new_feeding = form.save(commit=False)
    new_feeding.penguin_id = penguin_id
    new_feeding.save()
  return redirect('detail', penguin_id=penguin_id)

class ToyList(ListView):
  model = Toy

class ToyDetail(DetailView):
  model = Toy

class ToyCreate(CreateView):
  model = Toy
  fields = '__all__'

class ToyUpdate(UpdateView):
  model = Toy
  fields = ['name', 'color']

class ToyDelete(DeleteView):
  model = Toy
  success_url = '/toys/'

class PenguinCreate(CreateView):
  model = Penguin
  fields = '__all__'
  success_url = '/penguins/'

class PenguinUpdate(UpdateView):
  model = Penguin
  fields = ['breed', 'description', 'age']

class PenguinDelete(DeleteView):
  model = Penguin
  success_url = '/penguins/'

def assoc_toy(request, penguin_id, toy_id):
  Penguin.objects.get(id=penguin_id).toys.add(toy_id)
  return redirect('detail', penguin_id=penguin_id)

def add_photo(request, penguin_id):
  photo_file = request.FILES.get('photo-file', None)
  if photo_file:
    s3 = boto3.client('s3')
    key =uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
    try:
      s3.upload_fileobj(photo_file, BUCKET, key)
      url = f"{S3_BASE_URL}{BUCKET}/{key}"
      photo = Photo(url=url, penguin_id=penguin_id)
      photo.save()
    except Exception as err:
      print('An error occurred uploading file to S3: %s' % err)
  return redirect('detail', penguin_id=penguin_id)