from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions
from ..models.pays import Pays
from ..serializer.pays_serializer import PaysSerializer

# Create your views here.

class PaysViewSet(viewsets.ModelViewSet):
    queryset = Pays.objects.all()
    serializer_class = PaysSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]

    def get_queryset(self):
        return Pays.objects.all()