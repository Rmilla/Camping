from rest_framework import serializers
from ..models.pays import Pays

class PaysSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pays
        fields = '__all__'