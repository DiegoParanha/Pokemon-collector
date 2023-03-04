from django.db import models
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User

MEALS = (
    ('B', 'Breakfast'),
    ('L', 'Lunch'),
    ('D', 'Dinner')
)

# Create your models here.
class Move(models.Model):
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=20)
    color = models.CharField(max_length=20)

    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('moves_detail', kwargs={'pk': self.id})
    

class Pokemon(models.Model):
    name = models.CharField(max_length=100)
    number = models.IntegerField()
    type = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    ability = models.CharField(max_length=100)
    level = models.IntegerField()
    moves = models.ManyToManyField(Move)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} ({self.id})'
    
    def get_absolute_url(self):
        return reverse('detail', kwargs={'pokemon_id': self.id})
    
    def fed_for_today(self):
        return self.feeding_set.filter(date=date.today()).count() >= len(MEALS)
    
class Feeding(models.Model):
    date = models.DateField('Feeding Date')
    meal = models.CharField(
        max_length=1,
        choices=MEALS,
        default=MEALS[0][0]
        )
    
    pokemon = models.ForeignKey(
        Pokemon, 
        on_delete=models.CASCADE
    )
    
    def __str__(self):
        return f"{self.get_meal_display()} on {self.date}"
    
    class Meta:
        ordering = ['-date']


class Photo(models.Model):
    url = models.CharField(max_length=200)
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo for pokemon_id: {self.pokemon_id} @{self.url}"
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    favorite_color = models.CharField(max_length=50)