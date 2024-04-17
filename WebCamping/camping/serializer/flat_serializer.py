from rest_framework_mongoengine.serializers import DocumentSerializer
from ..models import Flat
from decimal import Decimal
from ..views.APImaps import distance_emissions 

class FlatSerializer(DocumentSerializer):
    class Meta:
        model = Flat
        fields = '__all__'

    def create(self, validated_data):
        # Extraire les données nécessaires pour le calcul
        start = validated_data.get('client_city')
        end = validated_data.get('city')
        mode = validated_data.get('transport_mode')

        # Calculer la distance et les émissions
        distance, emissions = distance_emissions(start, end, mode)

        # Ajouter les valeurs calculées aux données validées
        if distance is None or emissions is None:
            # Gérer le cas où distance_emissions retourne None pour l'une des valeurs
            raise ValueError("Unable to calculate distance and emissions.")
        
        validated_data['distance'] = distance
        validated_data['emission_total'] = Decimal(emissions)

        # Créer et retourner l'instance de Flat
        return super().create(validated_data)