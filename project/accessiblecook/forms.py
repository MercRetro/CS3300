from django.forms import ModelForm
from .models import Recipe, Ingredient

class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        fields = ['name', 'estimated_cook_time', 'instructions']

class IngredientForm(ModelForm):
    class Meta:
        model = Ingredient
        fields = ['name', 'recipe']