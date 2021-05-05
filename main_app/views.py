from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
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

@login_required
def penguins_index(request):
  penguins = Penguin.objects.filter(user=request.user)
  return render(request, 'penguins/index.html', { 'penguins': penguins })

@login_required
def penguins_detail(request, penguin_id):
  penguin = Penguin.objects.get(id=penguin_id)
  toys_penguin_doesnt_have = Toy.objects.exclude(id__in = penguin.toys.all().values_list('id'))
  feeding_form = FeedingForm()
  return render(request, 'penguins/detail.html', {
    'penguin': penguin, 'feeding_form': feeding_form,
    # Add the toys to be displayed
    'toys': toys_penguin_doesnt_have
  })

@login_required
def add_feeding(request, penguin_id):
  form = FeedingForm(request.POST)
  if form.is_valid():
    new_feeding = form.save(commit=False)
    new_feeding.penguin_id = penguin_id
    new_feeding.save()
  return redirect('detail', penguin_id=penguin_id)

class ToyList(LoginRequiredMixin, ListView):
  model = Toy

class ToyDetail(LoginRequiredMixin, DetailView):
  model = Toy

class ToyCreate(LoginRequiredMixin, CreateView):
  model = Toy
  fields = '__all__'

class ToyUpdate(LoginRequiredMixin, UpdateView):
  model = Toy
  fields = ['name', 'color']

class ToyDelete(LoginRequiredMixin, DeleteView):
  model = Toy
  success_url = '/toys/'

class PenguinCreate(LoginRequiredMixin, CreateView):
  model = Penguin
  fields = ['name', 'breed', 'description', 'age']

  def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)
  

class PenguinUpdate(LoginRequiredMixin, UpdateView):
  model = Penguin
  fields = ['breed', 'description', 'age']

class PenguinDelete(LoginRequiredMixin, DeleteView):
  model = Penguin
  success_url = '/penguins/'

@login_required
def assoc_toy(request, penguin_id, toy_id):
  Penguin.objects.get(id=penguin_id).toys.add(toy_id)
  return redirect('detail', penguin_id=penguin_id)

@login_required
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

def signup(request):
  error_message = ''
  if request.method == 'POST':
    # This is how to create a 'user' form object
    # that includes the data from the browser
    form = UserCreationForm(request.POST)
    if form.is_valid():
      # This will add the user to the database
      user = form.save()
      # This is how we log a user in via code
      login(request, user)
      return redirect('index')
    else:
      error_message = 'Invalid sign up - try again'
  # A bad POST or a GET request, so render signup.html with an empty form
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)  