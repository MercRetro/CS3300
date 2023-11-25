from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Recipe, Ingredient
from django.views import generic
from .forms import RecipeForm, IngredientForm

# Create your views here.

def index(request):
    recipes = Recipe.objects.all()
    return render(request, 'accessiblecook/index.html', {'recipes': recipes})

class RecipeListView(generic.ListView):
    model = Recipe
    template_name = 'recipes/recipe_list.html'
    context_object_name = 'recipes'

class RecipeDetailView(generic.DetailView):
    model = Recipe
    template_name = 'recipes/recipe_detail.html'
    context_object_name = 'recipe'

def add_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('recipe_list')
    else:
        form = RecipeForm()
    return render(request, 'recipes/add_recipe.html', {'form': form})

def add_ingredient(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    if request.method == 'POST':
        form = IngredientForm(request.POST)
        if form.is_valid():
            ingredient = form.save(commit=False)
            ingredient.recipe = recipe
            ingredient.save()
            return redirect('recipe_detail', pk=recipe_id)
    else:
        form = IngredientForm(initial={'recipe': recipe})
    return render(request, 'recipes/add_ingredient.html', {'form': form})