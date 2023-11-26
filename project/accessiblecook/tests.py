from django.test import TestCase
from django.urls import reverse
from .models import Recipe
from django.contrib.auth.models import User
from .views import add_recipe

class RecipeModelTests(TestCase):
    def test_recipe_creation(self):
        recipe = Recipe.objects.create(
            name="Test Recipe",
            estimated_cook_time="30 minutes",
            instructions="Test instructions.",
            ingredients="Test ingredients.",
        )
        self.assertEqual(Recipe.objects.count(), 1)
        self.assertEqual(str(recipe), recipe.name)

class RecipeCRUDTests(TestCase):
    def setUp(self):
        # Create a test user
        self.test_user = User.objects.create_user(username='admin', password='admin')

        # Create a test recipe
        self.test_recipe = Recipe.objects.create(
            name="Test Recipe",
            estimated_cook_time="30 minutes",
            instructions="Test instructions.",
            ingredients="Test ingredients.",

        )
    def test_add_recipe_view(self):
        response = self.client.get(reverse('add_recipe'))
        self.assertEqual(response.status_code, 302)  # Redirect if not logged in
    
    def test_add_recipe_view_auth(self):
        # Log in the test client
        self.client.login(username='admin', password='admin')
        response = self.client.get(reverse('add_recipe'))
        self.assertEqual(response.status_code, 200)
   
    def test_edit_recipe_view(self):
        # Log in the test client
        self.client.login(username='admin', password='admin')

        # Perform the request to edit the recipe
        response = self.client.get(reverse('edit_recipe', args=[self.test_recipe.pk]))

        # Check if the user is logged in and the response is successful (status code 200)
        self.assertEqual(response.status_code, 200)

        # Optionally, you can add more assertions to check specific content or form presence on the page

    def test_edit_recipe_form_submission(self):
        # Log in the test client
        self.client.login(username='admin', password='admin')

        # Prepare data for updating the recipe
        updated_data = {
            'name': 'Updated Recipe Name',
            'estimated_cook_time': '45 minutes',
            'instructions': 'Updated instructions.',
            'ingredients': 'Updated ingredients.',
        }

        # Perform the request to submit the updated form
        response = self.client.post(reverse('edit_recipe', args=[self.test_recipe.pk]), data=updated_data)

        # Check if the user is redirected to the detail view after successful form submission
        self.assertRedirects(response, reverse('recipe_detail', args=[self.test_recipe.pk]))

        # Optionally, you can check if the database has been updated with the new data
        updated_recipe = Recipe.objects.get(pk=self.test_recipe.pk)
        self.assertEqual(updated_recipe.name, updated_data['name'])
        self.assertEqual(updated_recipe.estimated_cook_time, updated_data['estimated_cook_time'])
        self.assertEqual(updated_recipe.instructions, updated_data['instructions'])
        self.assertEqual(updated_recipe.ingredients, updated_data['ingredients'])

    
    def test_remove_recipe_view(self):
        # Log in the test client
        self.client.login(username='admin', password='admin')

        # Perform the request to remove the recipe using a POST request
        response = self.client.post(reverse('remove_recipe', args=[self.test_recipe.pk]))

        # Check if the user is redirected to the recipe list after successful removal
        self.assertRedirects(response, reverse('recipe_list'))

        # Optionally, you can check if the recipe is no longer in the database
        with self.assertRaises(Recipe.DoesNotExist):
            Recipe.objects.get(pk=self.test_recipe.pk)
