from rest_framework import serializers
from ..models.camping import Camping

class CampingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Camping
        fields = '__all__'


            
        
