from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from django.contrib.auth.models import User
from .models import Recipe

class RecipeSeleniumTests(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = webdriver.Chrome(executable_path='C:\Program Files (x86)\chromedriver-win64')

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

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

        # Log in the test user
        self.selenium.get(self.live_server_url + '/login/')
        username_input = self.selenium.find_element_by_name("username")
        password_input = self.selenium.find_element_by_name("password")
        username_input.send_keys('testuser')
        password_input.send_keys('testpassword')
        password_input.send_keys(Keys.RETURN)

    def test_edit_recipe_selenium(self):
        # Navigate to the edit recipe page
        self.selenium.get(self.live_server_url + f'/recipes/{self.test_recipe.pk}/edit/')

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
        self.assertEqual(self.selenium.current_url, f'{self.live_server_url}/recipes/{self.test_recipe.pk}/')

        # Optionally, you can check if the database has been updated with the new data
        updated_recipe = Recipe.objects.get(pk=self.test_recipe.pk)
        self.assertEqual(updated_recipe.name, "Updated Recipe Name")
        self.assertEqual(updated_recipe.estimated_cook_time, "45 minutes")
        self.assertEqual(updated_recipe.instructions, "Updated instructions.")
        self.assertEqual(updated_recipe.ingredients, "Updated ingredients.")

    def test_remove_recipe_selenium(self):
        # Navigate to the remove recipe page
        self.selenium.get(self.live_server_url + f'/recipes/{self.test_recipe.pk}/remove/')

        # Perform actions with the Selenium WebDriver (e.g., click on confirmation button)
        self.selenium.find_element_by_id("confirm-button").click()

        # Assert that the user is redirected to the recipe list
        self.assertEqual(self.selenium.current_url, f'{self.live_server_url}/recipes/')

        # Optionally, you can check if the recipe is no longer in the database
        with self.assertRaises(Recipe.DoesNotExist):
            Recipe.objects.get(pk=self.test_recipe.pk)
