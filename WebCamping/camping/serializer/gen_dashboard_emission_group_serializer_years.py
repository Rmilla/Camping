from rest_framework import serializers

class General_emission_group_serializer_years(serializers.Serializer):
            y2013 = serializers.FloatField()
            y2014 = serializers.FloatField()
            y2015 = serializers.FloatField()
            y2016 = serializers.FloatField()
            y2017 = serializers.FloatField()
            y2018 = serializers.FloatField()
            y2019 = serializers.FloatField()
            y2020 = serializers.FloatField()
            y2021 = serializers.FloatField()
            y2022 = serializers.FloatField()
            y2023 = serializers.FloatField()

            class Meta:
                fields = ['y2013','y2014','y2015','y2016','y2017','y2018','y2019','y2020','y2021','y2022','y2023']