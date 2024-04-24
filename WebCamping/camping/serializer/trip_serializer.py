from ..models.camping import Trip
from rest_framework import serializers

class TripSerializer(serializers.Serializer):
    class Meta:
        model = Trip
        fields = '__all__'