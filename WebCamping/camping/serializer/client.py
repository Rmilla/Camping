from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from django.http import JsonResponse
from rest_framework.decorators import action
from rest_framework_mongoengine.serializers import DocumentSerializer
from rest_framework import viewsets, permissions
from ..models import Client

class ClientSerializer(DocumentSerializer):
    class Meta:
        model = Client
        fields = '__all__'

    def create(self, validated_data):
        return Client.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance