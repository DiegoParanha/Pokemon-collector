from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('pokemons/', views.pokemons_index, name='index'),
    path('pokemons/<int:pokemon_id>/', views.pokemons_detail, name='detail'),
    path('pokemons/create/', views.PokemonCreate.as_view(), name='pokemons_create'),
    path('pokemons/<int:pk>/update', views.PokemonUpdate.as_view(), name='pokemons_update'),
    path('pokemons/<int:pk>/delete', views.PokemonDelete.as_view(), name='pokemons_delete'),
    path('pokemons/<int:pokemon_id>/add_feeding', views.add_feeding, name='add_feeding'),
    path('pokemons/<int:pokemon_id>/assoc_move/<int:move_id>/', views.assoc_move, name='assoc_move'),
    path('pokemons/<int:pokemon_id>/unassoc_move/<int:move_id>/', views.unassoc_move, name='unassoc_move'),
    path('moves/', views.MoveList.as_view(), name='moves_index'),
    path('moves/<int:pk>/', views.MoveDetail.as_view(), name='moves_detail'),
    path('moves/create/', views.MoveCreate.as_view(), name='moves_create'),
    path('moves/<int:pk>/update/', views.MoveUpdate.as_view(), name='moves_update'),
    path('moves/<int:pk>/delete/', views.MoveDelete.as_view(), name='moves_delete'),
]