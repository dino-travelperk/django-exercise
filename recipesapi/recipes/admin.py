from django.contrib import admin
from recipes.models import Ingredient, Recipe


class IngredientInline(admin.TabularInline):
    model = Ingredient
    extra = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = [IngredientInline]
    list_display = ("name", "description", "get_ingredients")

    @admin.display(description="ingredients")
    def get_ingredients(self, obj):
        return ", ".join(e.name for e in obj.ingredients.all())
