from rest_framework import viewsets
from recipes.models import Recipe
from recipes import serializers


class RecipeViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.RecipeSerializer
    queryset = Recipe.objects.all().prefetch_related("ingredients")

    def get_queryset(self):
        name = self.request.query_params.get("name")
        if name:
            return self.queryset.filter(name__icontains=name)

        return super().get_queryset()
