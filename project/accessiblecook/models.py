from django.db import models
from django.urls import reverse


class Recipe(models.Model):
    name = models.CharField(max_length=255)
    estimated_cook_time = models.CharField(max_length=50)
    ingredients = models.TextField()
    instructions = models.TextField()
    

    def __str__(self):
        return self.name