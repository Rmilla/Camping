from rest_framework import serializers

class InserValue(serializers.Serializer):
            nom = serializers.CharField()
            ville_client = serializers.CharField()
            pays_client = serializers.CharField()
            vehicule = serializers.CharField()
            camping = serializers.CharField()
            ville_camping = serializers.CharField()
            date = serializers.DateField()
            class Meta:
                fields = '__all__'