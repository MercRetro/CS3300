from django.db import models
from django.urls import reverse

# Create your models here.

class Recipe(models.Model):
    name = models.CharField(max_length=255)
    estimated_cook_time = models.CharField(max_length=50)
    instructions = models.TextField()

    def __str__(self):
        return self.name

class Ingredient(models.Model):
    name = models.CharField(max_length=255)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.name


