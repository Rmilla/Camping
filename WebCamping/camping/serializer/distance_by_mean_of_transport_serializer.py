from rest_framework import serializers

class Distance_by_transport_Serializer(serializers.Serializer):
            vehicle = serializers.CharField()
            distances = serializers.ListField(child=serializers.FloatField())
            class Meta:
                fields = ['vehicle','distances']