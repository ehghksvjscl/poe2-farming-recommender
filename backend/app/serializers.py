from rest_framework import serializers

from app.models import FarmingMethod, MarketItem


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


class FarmingMethodListSerializer(serializers.ModelSerializer):
    """파밍 방법 목록용 시리얼라이저 (요약 정보)"""
    
    class Meta:
        model = FarmingMethod
        fields = [
            "id",
            "slug",
            "name",
            "name_ko",
            "category",
            "difficulty",
            "rating",
            "icon",
            "summary",
            "estimated_profit_min",
            "estimated_profit_max",
            "investment_required",
            "is_league_specific",
            "league",
            "creator_name",
        ]


class FarmingMethodDetailSerializer(serializers.ModelSerializer):
    """파밍 방법 상세용 시리얼라이저 (전체 정보)"""
    
    class Meta:
        model = FarmingMethod
        fields = [
            "id",
            "slug",
            "name",
            "name_ko",
            "category",
            "difficulty",
            "rating",
            "icon",
            "summary",
            "description",
            "requirements",
            "recommended_items",
            "steps",
            "tips",
            "estimated_profit_min",
            "estimated_profit_max",
            "investment_required",
            "is_league_specific",
            "league",
            "creator_name",
            "creator_url",
            "video_url",
            "source_url",
            "updated_at",
        ]
