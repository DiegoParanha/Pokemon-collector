from django.shortcuts import render
from.models import Pokemon

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
   return render(request, 'pokemons/detail.html', { 'pokemon': pokemon })