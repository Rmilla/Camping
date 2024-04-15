from rest_framework import viewsets
from ..models import Flat
from ..serializer.flat_serializer import FlatSerializer

class SnippetViewSet(viewsets.ModelViewSet):
    queryset = Flat.objects.all()
    serializer_class = FlatSerializer