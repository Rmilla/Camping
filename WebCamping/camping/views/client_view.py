from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from django.http import JsonResponse
from rest_framework.decorators import action
from rest_framework_mongoengine.serializers import DocumentSerializer
from rest_framework import viewsets, permissions
from ..models import Client
from camping.serializer.client_serializer import ClientSerializer   

# Create your views here.
   
class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    #filterset_class = ClubFilters

    def get_queryset(self):
        return Client.objects.all()