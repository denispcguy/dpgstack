from rest_framework import serializers
from .models import BlueprintSimpleModel


class BlueprintSimpleModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlueprintSimpleModel
        fields = ['id', 'name', 'description']