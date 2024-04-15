from rest_framework_mongoengine.serializers import DocumentSerializer
from ..models import Flat
from ..views.APImaps import distance_emissions # Assurez-vous que le chemin d'importation est correct

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
        validated_data['distance'] = distance
        validated_data['emission_total'] = emissions

        # Créer et retourner l'instance de Flat
        return super().create(validated_data)