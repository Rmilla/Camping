from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from django.http import JsonResponse
from rest_framework import viewsets, permissions
from ..models.adresse import Adresse_camping
from camping.serializer.adresse_serializer import AdresseSerializer

# Create your views here.

class AdresseViewSet(viewsets.ModelViewSet):
    queryset = Adresse_camping.objects.all()
    serializer_class = AdresseSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]

    def get_queryset(self):
        return Adresse_camping.objects.all()