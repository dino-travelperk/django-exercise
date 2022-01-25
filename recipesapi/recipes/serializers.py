from rest_framework import serializers
from recipes.models import Recipe, Ingredient


class IngredientSerializer(serializers.ModelSerializer):
    """Serializer for the Ingredient objects"""

    class Meta:
        model = Ingredient
        fields = ("name",)


class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for Recipe objects"""

    ingredients = IngredientSerializer(many=True)

    class Meta:
        model = Recipe
        fields = (
            "id",
            "name",
            "description",
            "ingredients",
        )
        read_only_fields = ("id",)

    def create(self, validated_data):
        ingredients = validated_data.pop("ingredients")
        recipe = super().create(validated_data)

        for unique_ingredient in {ingredient["name"]: ingredient for ingredient in ingredients}.values():
            recipe.ingredients.create(**unique_ingredient)

        return recipe

    def update(self, instance, validated_data):
        ingredients = validated_data.pop("ingredients", None)
        recipe = super().update(instance, validated_data)

        if ingredients:
            recipe.ingredients.all().delete()
            for unique_ingredient in {ingredient["name"]: ingredient for ingredient in ingredients}.values():
                recipe.ingredients.create(**unique_ingredient)

        return recipe
