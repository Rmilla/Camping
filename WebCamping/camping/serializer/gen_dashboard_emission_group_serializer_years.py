from rest_framework import serializers

class General_emission_group_serializer_years(serializers.ModelSerializer):
    class Meta:
        fields = [
            "2014",
            "2015",
            "2016",
            "2017",
            "2018",
            "2019",
            "2020",
            "2021",
            "2022",
            "2023",
            "2024",
        ]