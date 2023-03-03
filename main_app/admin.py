from django.contrib import admin
from .models import Pokemon, Feeding, Move, Photo

# Register your models here.
admin.site.register(Pokemon)

admin.site.register(Feeding)

admin.site.register(Move)

admin.site.register(Photo)

