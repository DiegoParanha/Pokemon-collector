import os
import uuid
import boto3
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import FeedingForm
from.models import Pokemon, Move, Photo

# pokemons = [
#    {'name': 'Squirtle', 'number': '007', 'type':'Water', 'description': 'Tiny Turtle', 'ability': 'Torrent', 'level': 1},
#    {'name': 'Charmander', 'number': '004', 'type':'Fire', 'description': 'Lizard Pokemon', 'ability': 'Blaze', 'level': 1},
# ]

# Create your views here.

def home(request):
    return render(request, 'home.html')

def about(request):
  return render(request, 'about.html')

@login_required
def pokemons_index(request):
  pokemons = Pokemon.objects.filter(user=request.user)
  return render(request, 'pokemons/index.html', {
    'pokemons': pokemons
  })

@login_required
def pokemons_detail(request, pokemon_id):
   pokemon = Pokemon.objects.get(id=pokemon_id)
   id_list = pokemon.moves.all().values_list('id')
   moves_pokemon_doesnt_have = Move.objects.exclude(id__in=id_list)
   feeding_form = FeedingForm()
   return render(request, 'pokemons/detail.html', { 
      'pokemon': pokemon, 'feeding_form': feeding_form,
      'moves': moves_pokemon_doesnt_have
   })

class PokemonCreate(LoginRequiredMixin, CreateView):
   model = Pokemon
   fields = ['name', 'number', 'type', 'description', 'ability', 'level']

   def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)  

class PokemonUpdate(LoginRequiredMixin, UpdateView):
   model = Pokemon
   fields = ['name', 'number', 'type', 'description', 'ability', 'level']

class PokemonDelete(LoginRequiredMixin, DeleteView):
   model = Pokemon
   success_url = '/pokemons'

@login_required
def add_feeding(request, pokemon_id):
  form = FeedingForm(request.POST)
  if form.is_valid():
    new_feeding = form.save(commit=False)
    new_feeding.pokemon_id = pokemon_id
    new_feeding.save()
  return redirect('detail', pokemon_id=pokemon_id)

class MoveList(LoginRequiredMixin, ListView):
   model = Move

class MoveDetail(LoginRequiredMixin, DetailView):
   model = Move

class MoveCreate(LoginRequiredMixin, CreateView):
  model = Move
  fields = '__all__'

class MoveUpdate(LoginRequiredMixin, UpdateView):
  model = Move
  fields = ['name', 'type', 'color']

class MoveDelete(LoginRequiredMixin, DeleteView):
  model = Move
  success_url = '/moves'

@login_required
def assoc_move(request, pokemon_id, move_id):
  Pokemon.objects.get(id=pokemon_id).moves.add(move_id)
  return redirect('detail', pokemon_id=pokemon_id)

@login_required
def unassoc_move(request, pokemon_id, move_id):
  Pokemon.objects.get(id=pokemon_id).moves.remove(move_id)
  return redirect('detail', pokemon_id=pokemon_id)

@login_required
def add_photo(request, pokemon_id):
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        try:
            bucket = os.environ['S3_BUCKET']
            s3.upload_fileobj(photo_file, bucket, key)
            url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
            Photo.objects.create(url=url, pokemon_id=pokemon_id)
        except Exception as e:
            print('An error occurred uploading file to S3')
            print(e)
    return redirect('detail', pokemon_id=pokemon_id)

def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('index')
    else:
      error_message = 'Invalid sign up - Try Again'
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)