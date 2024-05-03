from rest_framework import serializers
from ..models.adresse import Adresse_camping

class AdresseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Adresse_camping
        fields = '__all__'