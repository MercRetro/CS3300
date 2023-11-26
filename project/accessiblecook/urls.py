# accessiblecook/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from .views import (
    index,
    RecipeListView,
    RecipeDetailView,    
    add_recipe,
    edit_recipe,
    remove_recipe,
    account_profile,
    CustomLogoutView,
    register_view,
)

urlpatterns = [
    path('', index, name='index'),
    path('recipes/', RecipeListView.as_view(), name='recipe_list'),
    path('recipes/<int:pk>/', RecipeDetailView.as_view(), name='recipe_detail'),
    path('recipes/add/', add_recipe, name='add_recipe'),
    path('recipes/<int:recipe_id>/edit/', edit_recipe, name='edit_recipe'),
    path('recipes/<int:recipe_id>/remove/', remove_recipe, name='remove_recipe'),

    # Account
    path('accounts/profile/', account_profile, name='account_profile'),

    # Authentication views
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('register/', register_view, name='register'),
]
