from rest_framework import serializers

class Pie_chart_serializer(serializers.Serializer):
    belle_plage=serializers.FloatField()
    blue_bayou=serializers.FloatField()
    cap_sud=serializers.FloatField()
    valencia=serializers.FloatField()

    class Meta:
                fields = ["belle_plage", "blue_bayou", "cap_sud", "valencia"]