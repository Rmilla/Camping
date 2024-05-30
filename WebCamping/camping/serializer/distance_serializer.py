from ..models.distance import EstDistant
from rest_framework import serializers

class DistanceSerializer(serializers.Serializer):
    class Meta:
        model = EstDistant
        fields = '__all__'  