from rest_framework import serializers
from ..models.camping import Camping
from ..models.trip import Trip

class CampingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Camping
        fields = '__all__'


            
        
