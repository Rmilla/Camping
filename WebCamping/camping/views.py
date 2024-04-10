from django.shortcuts import render
from rest_framework_mongoengine.serializers import DocumentSerializer
from rest_framework import serializers
from .models import Camping

# Create your views here.


class CampingSerializer(DocumentSerializer):
    class Meta:
        model = Camping
        fields = '__all__'

    def create(self, validated_data):
        return Camping.objects.all()

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
    
class CampingViewSet(viewsets.ModelViewSet):
    queryset = Camping.objects.all()
    serializer_class = CampingSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    #filterset_class = ClubFilters

class CampingViewSet(ModelViewSet):
    serializer_class = CampingSerializer

    def get_queryset(self):
        return Camping.objects.all()