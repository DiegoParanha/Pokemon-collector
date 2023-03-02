from django.contrib import admin
from .models import Pokemon, Feeding, Move

# Register your models here.
admin.site.register(Pokemon)

admin.site.register(Feeding)

admin.site.register(Move)

