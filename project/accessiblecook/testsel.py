from django.test import LiveServerTestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Recipe
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

class RecipeSeleniumTests(LiveServerTestCase):
    def setUp(self):
        # Create a test user
        self.test_user = User.objects.create_user(username='testuser', password='testpassword')

        # Create a test recipe
        self.test_recipe = Recipe.objects.create(
            name="Test Recipe",
            estimated_cook_time="30 minutes",
            instructions="Test instructions.",
            ingredients="Test ingredients.",
        )

        # Set up Chrome options
        chrome_options = Options()
        chrome_options.add_argument('C:\Program Files (x86)\chromedriver-win64')

        # Initialize Chrome WebDriver with options
        self.selenium = webdriver.Chrome(options=chrome_options)

        # Log in the test user
        login_url = reverse('login')
        self.selenium.get(self.live_server_url + login_url)
        username_input = self.selenium.find_element_by_name("username")
        password_input = self.selenium.find_element_by_name("password")
        username_input.send_keys('testuser')
        password_input.send_keys('testpassword')
        password_input.send_keys(Keys.RETURN)

    def tearDown(self):
        self.selenium.quit()

    def test_edit_recipe_selenium(self):
        # Navigate to the edit recipe page
        edit_recipe_url = reverse('edit_recipe', args=[self.test_recipe.pk])
        self.selenium.get(self.live_server_url + edit_recipe_url)
        # Perform actions with the Selenium WebDriver (e.g., fill out form, submit)
        name_input = self.selenium.find_element_by_name("name")
        estimated_cook_time_input = self.selenium.find_element_by_name("estimated_cook_time")
        instructions_input = self.selenium.find_element_by_name("instructions")
        ingredients_input = self.selenium.find_element_by_name("ingredients")

        name_input.clear()
        estimated_cook_time_input.clear()
        instructions_input.clear()
        ingredients_input.clear()

        name_input.send_keys("Updated Recipe Name")
        estimated_cook_time_input.send_keys("45 minutes")
        instructions_input.send_keys("Updated instructions.")
        ingredients_input.send_keys("Updated ingredients.")

        # Submit the form
        self.selenium.find_element_by_id("submit-button").click()

        # Assert that the user is redirected to the detail view
        self.assertEqual(self.selenium.current_url, self.live_server_url + reverse('recipe_detail', args=[self.test_recipe.pk]))

        # Optionally, you can check if the database has been updated with the new data
        updated_recipe = Recipe.objects.get(pk=self.test_recipe.pk)
        self.assertEqual(updated_recipe.name, "Updated Recipe Name")
        self.assertEqual(updated_recipe.estimated_cook_time, "45 minutes")
        self.assertEqual(updated_recipe.instructions, "Updated instructions.")
        self.assertEqual(updated_recipe.ingredients, "Updated ingredients.")

    def test_remove_recipe_selenium(self):
        # Navigate to the remove recipe page
        self.selenium.get(self.live_server_url + reverse('remove_recipe', args=[self.test_recipe.pk]))

        # Perform actions with the Selenium WebDriver (e.g., click on confirmation button)
        self.selenium.find_element_by_id("confirm-button").click()

        # Assert that the user is redirected to the recipe list
        self.assertEqual(self.selenium.current_url, self.live_server_url + reverse('recipe_list'))

        # Optionally, you can check if the recipe is no longer in the database
        with self.assertRaises(Recipe.DoesNotExist):
            Recipe.objects.get(pk=self.test_recipe.pk)
