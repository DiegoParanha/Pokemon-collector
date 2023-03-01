from django.db import models

# Create your models here.

class Pokemon(models.Model):
    name = models.CharField(max_length=100)
    number = models.IntegerField()
    type = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    ability = models.CharField(max_length=100)
    level = models.IntegerField()

    def __str__(self):
        return f'{self.name} ({self.id})'