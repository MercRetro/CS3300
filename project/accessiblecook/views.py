from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Recipe
from django.views import generic
from django.urls import reverse_lazy
from .forms import RecipeForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LogoutView as AuthLogoutView, PasswordResetView
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test


# Create your views here.

def index(request):
    recipes = Recipe.objects.all()
    return render(request, 'accessiblecook/index.html', {'recipes': recipes})

class RecipeListView(generic.ListView):
    model = Recipe
    template_name = 'accessiblecook/recipe_list.html'
    context_object_name = 'recipes'
    
class RecipeDetailView(generic.DetailView):
    model = Recipe
    template_name = 'accessiblecook/recipe_detail.html'
    context_object_name = 'recipe'
    

def user_is_authenticated(user):
    return user.is_authenticated

@user_passes_test(user_is_authenticated)
def add_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('recipe_list')
    else:
        form = RecipeForm()
    return render(request, 'accessiblecook/add_recipe.html', {'form': form})

@user_passes_test(user_is_authenticated)
def edit_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    if request.method == 'POST':
        form = RecipeForm(request.POST, instance=recipe)
        if form.is_valid():
            form.save()
            return redirect('recipe_detail', pk=recipe_id)
    else:
        form = RecipeForm(instance=recipe)
    return render(request, 'accessiblecook/edit_recipe.html', {'form': form, 'recipe': recipe})


@user_passes_test(user_is_authenticated)
def remove_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    if request.method == 'POST':
        recipe.delete()
        return redirect('recipe_list')
    return render(request, 'accessiblecook/remove_recipe.html', {'recipe': recipe})

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')  # Redirect to the home page after registration
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def account_profile(request):
    # Your view logic here
    return render(request, 'accessiblecook/account_profile.html')

class CustomLogoutView(AuthLogoutView):
    template_name = 'registration/logout.html'
