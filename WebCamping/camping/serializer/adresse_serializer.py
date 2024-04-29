from rest_framework import serializers
from ..models.adresse import Adresse_camping

class AdresseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Adresse_camping
        fields = '__all__'

    # def create(self, validated_data):
    #     return Adresse_camping.objects.create(**validated_data)

    # def update(self, instance, validated_data):
    #     for attr, value in validated_data.items():
    #         setattr(instance, attr, value)
    #     instance.save()
    #     return instance