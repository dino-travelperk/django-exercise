from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from recipes.models import Ingredient, Recipe
import json


def sample_recipe_with_ingredients(**params):
    defaults = {
        "name": "sample recipe",
        "description": "sample recipe description",
    }
    defaults.update(params)

    recipe = Recipe.objects.create(**defaults)

    recipe.ingredients.create(name="dough")
    recipe.ingredients.create(name="cheese")
    recipe.ingredients.create(name="tomato")

    return recipe


class ApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_retrieve_recipes(self):
        sample_recipe_with_ingredients(name="pizza")
        sample_recipe_with_ingredients(name="calzone")

        response = self.client.get("/recipes/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_retrieve_filtered_recipes(self):
        sample_recipe_with_ingredients(name="pizza")
        sample_recipe_with_ingredients(name="calzone")

        response = self.client.get("/recipes/?name=za")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_recipe(self):
        recipe = sample_recipe_with_ingredients()

        response = self.client.get(f"/recipes/{recipe.id}/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], recipe.name)

    def test_create_recipe(self):
        payload = {
            "name": "pizza margharita",
            "description": "tastes awesome",
            "ingredients": [
                {"name": "dough"},
                {"name": "cheese"},
                {"name": "tomato"},
                {"name": "basil"},
            ],
        }

        response = self.client.post(
            "/recipes/",
            data=json.dumps(payload),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        recipe = Recipe.objects.get(id=response.data["id"])
        self.assertEqual(response.data["name"], recipe.name)
        self.assertEqual(len(response.data["ingredients"]), recipe.ingredients.count())

    def test_put_recipe(self):
        recipe = sample_recipe_with_ingredients(name="original recipe")

        payload = {
            "name": "pizza margharita",
            "description": "tastes awesome",
            "ingredients": [
                {"name": "dough"},
                {"name": "cheese"},
                {"name": "tomato"},
                {"name": "basil"},
            ],
        }

        response = self.client.put(
            f"/recipes/{recipe.id}/",
            data=json.dumps(payload),
            content_type="application/json",
        )

        updated_recipe = Recipe.objects.get(id=recipe.id)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(updated_recipe.ingredients.count(), 4)
        self.assertEqual(updated_recipe.name, payload["name"])

    def test_patch_recipe(self):
        recipe = sample_recipe_with_ingredients(name="original recipe")

        payload = {
            "ingredients": [
                {"name": "dough"},
                {"name": "cheese"},
                {"name": "tomato"},
                {"name": "basil"},
            ],
        }

        response = self.client.patch(
            f"/recipes/{recipe.id}/",
            data=json.dumps(payload),
            content_type="application/json",
        )

        updated_recipe = Recipe.objects.get(id=recipe.id)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(updated_recipe.ingredients.count(), 4)
        self.assertEqual(updated_recipe.name, recipe.name)

    def test_delete_recipe(self):
        recipe = sample_recipe_with_ingredients()
        response = self.client.delete(f"/recipes/{recipe.id}/")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Recipe.objects.count(), 0)
        self.assertEqual(Ingredient.objects.count(), 0)
