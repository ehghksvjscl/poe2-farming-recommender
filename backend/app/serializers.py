from rest_framework import serializers

from app.models import MarketItem


class MarketItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarketItem
        fields = [
            "id",
            "item_id",
            "name",
            "name_ko",
            "type",
            "category",
            "icon_url",
            "current_price",
            "league",
            "updated_at",
        ]


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


class ContentPreferenceSerializer(serializers.Serializer):
    key = serializers.CharField()
    label = serializers.CharField()
    description = serializers.CharField()
    icon_url = serializers.URLField()
    sort_order = serializers.IntegerField()
