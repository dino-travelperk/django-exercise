from django.test import TestCase
from recipes.models import Ingredient, Recipe
from recipes.serializers import RecipeSerializer


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


class SerializersTests(TestCase):
    def test_create_recipe(self):
        data = {
            "name": "pizza margharita",
            "description": "tastes awesome",
            "ingredients": [
                {"name": "dough"},
                {"name": "cheese"},
                {"name": "tomato"},
                {"name": "basil"},
            ],
        }

        serializer = RecipeSerializer(data=data)

        self.assertTrue(serializer.is_valid())

        serializer.save()

        self.assertEqual(Recipe.objects.count(), 1)
        self.assertEqual(Ingredient.objects.count(), 4)

    def test_update_recipe(self):
        recipe = sample_recipe_with_ingredients()

        data = {
            "name": "pizza margharita",
            "description": "tastes awesome",
            "ingredients": [
                {"name": "dough"},
                {"name": "cheese"},
                {"name": "tomato"},
                {"name": "basil"},
            ],
        }

        serializer = RecipeSerializer(recipe, data=data)

        self.assertTrue(serializer.is_valid())

        serializer.save()

        self.assertEqual(Recipe.objects.count(), 1)
        self.assertEqual(Ingredient.objects.count(), 4)

    def test_serialize_recipe(self):
        recipe = sample_recipe_with_ingredients()

        serializer = RecipeSerializer(recipe)

        self.assertEqual(serializer.data["id"], recipe.id)
        self.assertEqual(serializer.data["name"], recipe.name)
        self.assertEqual(len(serializer.data["ingredients"]), recipe.ingredients.count())
