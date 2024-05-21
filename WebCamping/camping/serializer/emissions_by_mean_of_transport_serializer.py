from rest_framework import serializers

class Emission_by_transport_Serializer(serializers.Serializer):
            vehicle = serializers.CharField()
            emissions = serializers.ListField(child=serializers.FloatField())
            class Meta:
                fields = ['vehicle','emissions']