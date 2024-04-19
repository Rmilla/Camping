from rest_framework_mongoengine.serializers import DocumentSerializer
from ..models.addresse import Adress_camping

class CampingSerializer(DocumentSerializer):
    class Meta:
        model = Adress_camping
        fields = '__all__'

    def create(self, validated_data):
        return Adress_camping.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance