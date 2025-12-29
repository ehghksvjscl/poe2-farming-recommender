from rest_framework.response import Response
from rest_framework.views import APIView

from app.models import ContentPreference, FarmingMethod, MarketItem
from app.recommend import RecommendationInput, build_recommendations
from app.serializers import (
    ContentPreferenceSerializer,
    FarmingMethodListSerializer,
    FarmingMethodDetailSerializer,
    MarketItemSerializer,
    RecommendationSerializer,
)


class RecommendationAPIView(APIView):
    def post(self, request):
        preferred_content = request.data.get("preferred_content", [])
        if isinstance(preferred_content, str):
            preferred_content = [c.strip() for c in preferred_content.split(",") if c.strip()]
        
        payload = RecommendationInput(
            preferred_content=preferred_content,
            profit_goal=request.data.get("profit_goal", "medium"),
            investment=request.data.get("investment", "low"),
            league=request.data.get("league", "Fate of the Vaal"),
        )
        recommendations = build_recommendations(payload)
        serializer = RecommendationSerializer(recommendations, many=True)
        return Response({"results": serializer.data})


class ContentPreferenceAPIView(APIView):
    def get(self, request):
        preferences = ContentPreference.objects.all()
        serializer = ContentPreferenceSerializer(preferences, many=True)
        return Response({"results": serializer.data})


class MarketItemListAPIView(APIView):
    """1 디바인/엑잘 이상 아이템 리스트 API
    
    NOTE: poe2scout의 모든 가격은 Exalted Orb 기준입니다.
    - current_price = Exalted Orb 기준 가격
    - Divine Orb의 current_price = 1 Divine이 몇 Exalted인지
    """

    def get(self, request):
        min_price = request.query_params.get("min_price", 1)
        price_unit = request.query_params.get("unit", "exalted")  # "exalted" or "divine"
        category = request.query_params.get("category")
        search = request.query_params.get("search")

        try:
            min_price = float(min_price)
        except (ValueError, TypeError):
            min_price = 1

        # Divine Orb 가격 조회 (= 1 Divine이 몇 Exalted인지)
        divine_item = MarketItem.objects.filter(name="Divine Orb").first()
        divine_in_exalted = float(divine_item.current_price) if divine_item and divine_item.current_price else 459.0

        # 기준 화폐에 따른 최소 가격 계산 (Exalted 기준으로 변환)
        if price_unit == "divine":
            # N Divine = N * divine_in_exalted Exalted
            min_exalted_price = min_price * divine_in_exalted
        else:  # exalted
            min_exalted_price = min_price

        queryset = MarketItem.objects.filter(
            current_price__gte=min_exalted_price
        ).exclude(name="")

        if category:
            queryset = queryset.filter(category=category)

        if search:
            from django.db.models import Q
            queryset = queryset.filter(
                Q(name__icontains=search) | Q(name_ko__icontains=search)
            )

        # 가격순 정렬
        queryset = queryset.order_by("-current_price")

        # 아이템에 환산 가격 추가
        items_data = []
        for item in queryset:
            item_data = MarketItemSerializer(item).data
            # current_price는 이미 Exalted 기준
            price_in_exalted = float(item.current_price) if item.current_price else 0
            # Divine 환산: Exalted 가격 / (1 Divine당 Exalted 수)
            price_in_divine = price_in_exalted / divine_in_exalted if divine_in_exalted else 0
            
            item_data["price_in_exalted"] = round(price_in_exalted, 2)
            item_data["price_in_divine"] = round(price_in_divine, 2)
            items_data.append(item_data)

        # 카테고리별 통계
        categories = (
            MarketItem.objects.filter(current_price__gte=min_exalted_price)
            .exclude(name="")
            .values_list("category", flat=True)
            .distinct()
        )

        return Response({
            "count": len(items_data),
            "min_price": min_price,
            "price_unit": price_unit,
            "exchange_rates": {
                "exalted_per_divine": round(divine_in_exalted, 2),
            },
            "categories": list(set(categories)),
            "items": items_data,
        })


class FarmingMethodListAPIView(APIView):
    """파밍 방법 목록 API"""

    def get(self, request):
        category = request.query_params.get("category")
        difficulty = request.query_params.get("difficulty")
        league_specific = request.query_params.get("league_specific")

        queryset = FarmingMethod.objects.filter(is_active=True)

        if category:
            queryset = queryset.filter(category=category)

        if difficulty:
            queryset = queryset.filter(difficulty=difficulty)

        if league_specific is not None:
            is_league_specific = league_specific.lower() in ("true", "1", "yes")
            queryset = queryset.filter(is_league_specific=is_league_specific)

        queryset = queryset.order_by("sort_order", "-estimated_profit_max")

        serializer = FarmingMethodListSerializer(queryset, many=True)

        # 카테고리별 통계
        categories = list(
            FarmingMethod.objects.filter(is_active=True)
            .values_list("category", flat=True)
            .distinct()
        )

        # 난이도별 통계
        difficulties = list(
            FarmingMethod.objects.filter(is_active=True)
            .values_list("difficulty", flat=True)
            .distinct()
        )

        return Response({
            "count": queryset.count(),
            "categories": categories,
            "difficulties": difficulties,
            "methods": serializer.data,
        })


class FarmingMethodDetailAPIView(APIView):
    """파밍 방법 상세 API"""

    def get(self, request, slug):
        try:
            method = FarmingMethod.objects.get(slug=slug, is_active=True)
        except FarmingMethod.DoesNotExist:
            return Response({"error": "파밍 방법을 찾을 수 없습니다."}, status=404)

        serializer = FarmingMethodDetailSerializer(method)
        return Response(serializer.data)
