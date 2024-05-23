from rest_framework import serializers

class General_emission_group_serializer_years(serializers.Serializer):
            year = serializers.IntegerField()
            emissions = serializers.FloatField()
            class Meta:
                fields = ['year','emissions']