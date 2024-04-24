from rest_framework import serializers
from ..models.camping import Camping
from ..models.camping import Trip

class CampingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Camping
        fields = '__all__'

    # def create(self, validated_data):
    #     return Camping.objects.create(**validated_data)

    # def update(self, instance, validated_data):
    #     for attr, value in validated_data.items():
    #         setattr(instance, attr, value)
    #     instance.save()
    #     return instance


            
        
