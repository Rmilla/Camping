from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from django.http import JsonResponse
from rest_framework.decorators import action
from rest_framework_mongoengine.serializers import DocumentSerializer
from rest_framework import viewsets, permissions
from ..models import Camping

class CampingSerializer(DocumentSerializer):
    class Meta:
        model = Camping
        fields = '__all__'

    def create(self, validated_data):
        return Camping.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance