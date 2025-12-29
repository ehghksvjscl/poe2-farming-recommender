from rest_framework.response import Response
from rest_framework.views import APIView

from app.recommend import RecommendationInput, build_recommendations
from app.serializers import RecommendationSerializer


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
