from django.shortcuts import render
from rest_framework_mongoengine.serializers import DocumentSerializer
from rest_framework import serializers
from .models import Camping

# Create your views here.


campings = Camping.objects.all()
class CampingSerializer(DocumentSerializer):
    class Meta:
        model = Camping
        fields = '__all__'

    def create(self, validated_data):
        return campings

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance