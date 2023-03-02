from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from.models import Pokemon, Move
from .forms import FeedingForm

# pokemons = [
#    {'name': 'Squirtle', 'number': '007', 'type':'Water', 'description': 'Tiny Turtle', 'ability': 'Torrent', 'level': 1},
#    {'name': 'Charmander', 'number': '004', 'type':'Fire', 'description': 'Lizard Pokemon', 'ability': 'Blaze', 'level': 1},
# ]

# Create your views here.

def home(request):
    return render(request, 'home.html')

def about(request):
  return render(request, 'about.html')

def pokemons_index(request):
  pokemons = Pokemon.objects.all()
  return render(request, 'pokemons/index.html', {
    'pokemons': pokemons
  })

def pokemons_detail(request, pokemon_id):
   pokemon = Pokemon.objects.get(id=pokemon_id)
   id_list = pokemon.moves.all().values_list('id')
   moves_pokemon_doesnt_have = Move.objects.exclude(id__in=id_list)
   feeding_form = FeedingForm()
   return render(request, 'pokemons/detail.html', { 
      'pokemon': pokemon, 'feeding_form': feeding_form,
      'moves': moves_pokemon_doesnt_have
   })

class PokemonCreate(CreateView):
   model = Pokemon
   fields = ['name', 'number', 'type', 'description', 'ability', 'level']

class PokemonUpdate(UpdateView):
   model = Pokemon
   fields = ['name', 'number', 'type', 'description', 'ability', 'level']

class PokemonDelete(DeleteView):
   model = Pokemon
   success_url = '/pokemons'

def add_feeding(request, pokemon_id):
  form = FeedingForm(request.POST)
  if form.is_valid():
    new_feeding = form.save(commit=False)
    new_feeding.pokemon_id = pokemon_id
    new_feeding.save()
  return redirect('detail', pokemon_id=pokemon_id)

class MoveList(ListView):
   model = Move

class MoveDetail(DetailView):
   model = Move

class MoveCreate(CreateView):
  model = Move
  fields = '__all__'

class MoveUpdate(UpdateView):
  model = Move
  fields = ['name', 'type', 'color']

class MoveDelete(DeleteView):
  model = Move
  success_url = '/moves'

def assoc_move(request, pokemon_id, move_id):
  Pokemon.objects.get(id=pokemon_id).moves.add(move_id)
  return redirect('detail', pokemon_id=pokemon_id)

def unassoc_move(request, pokemon_id, move_id):
  Pokemon.objects.get(id=pokemon_id).moves.remove(move_id)
  return redirect('detail', pokemon_id=pokemon_id)