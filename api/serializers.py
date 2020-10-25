from rest_framework import serializers
import uuid
from .models import Person

class PersonSerializer(serializers.Serializer):
    name = serializers.CharField()
    surname = serializers.CharField()

    def create(self, validated_data):
        return Person.objects.create(**validated_data)

class IdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ('ID',)