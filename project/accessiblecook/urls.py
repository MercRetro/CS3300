# accessiblecook/urls.py
from django.urls import path
from .views import RecipeListView, RecipeDetailView, add_recipe, add_ingredient, index

urlpatterns = [
    path('', index, name='index'),
    path('recipes/', RecipeListView.as_view(), name='recipe_list'),
    path('recipes/<int:pk>/', RecipeDetailView.as_view(), name='recipe_detail'),
    path('recipes/add/', add_recipe, name='add_recipe'),
    path('recipes/<int:recipe_id>/add_ingredient/', add_ingredient, name='add_ingredient'),
]
