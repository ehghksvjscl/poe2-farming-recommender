from rest_framework import serializers


class RecommendationSerializer(serializers.Serializer):
    zone = serializers.CharField()
    league = serializers.CharField()
    avg_profit_per_hour = serializers.CharField()
    drop_focus = serializers.CharField()
    allowed_builds = serializers.ListField(child=serializers.CharField())
    reason = serializers.CharField()
