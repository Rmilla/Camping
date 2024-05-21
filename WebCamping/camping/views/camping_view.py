from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from django.http import JsonResponse
from rest_framework import viewsets, permissions
from ..models.camping import Camping
from camping.serializer.camping_serializer import CampingSerializer

# Create your views here.

class CampingViewSet(viewsets.ModelViewSet):
    queryset = Camping.objects.all()
    serializer_class = CampingSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]

    def get_queryset(self):
        return Camping.objects.all()