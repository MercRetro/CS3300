from django.forms import ModelForm, modelformset_factory
from .models import Recipe

class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        fields = ['name', 'estimated_cook_time', 'ingredients', 'instructions']
