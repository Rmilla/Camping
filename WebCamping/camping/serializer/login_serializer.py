from rest_framework import serializers
from ..models.login import Login

class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = Login
        fields = '__all__'
        #username=serializers.ModelSerializer(source="user.username",read_only=True)