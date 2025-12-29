from rest_framework import serializers


class RecommendationSerializer(serializers.Serializer):
    zone = serializers.CharField()
    league = serializers.CharField()
    avg_profit_per_hour = serializers.CharField()
    drop_focus = serializers.CharField()
    reason = serializers.CharField()
    investment = serializers.CharField()
    strategy = serializers.CharField(required=False, allow_null=True)
    requirements = serializers.CharField(required=False, allow_null=True)
    tips = serializers.CharField(required=False, allow_null=True)
