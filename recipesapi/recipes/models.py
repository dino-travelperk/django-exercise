from django.db import models


class Recipe(models.Model):
    """Recipe"""

    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)


class Ingredient(models.Model):
    """Ingredient used by a recipe"""

    name = models.CharField(max_length=255)
    recipe = models.ForeignKey(
        to=Recipe,
        related_name="ingredients",
        on_delete=models.CASCADE,
    )
