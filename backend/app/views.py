from rest_framework.response import Response
from rest_framework.views import APIView

from app.recommend import RecommendationInput, build_recommendations
from app.serializers import RecommendationSerializer


class RecommendationAPIView(APIView):
    def post(self, request):
        payload = RecommendationInput(
            level=int(request.data.get("level", 1)),
            build_type=request.data.get("build_type", "알 수 없음"),
            preferred_content=request.data.get("preferred_content", "맵핑"),
        )
        recommendations = build_recommendations(payload)
        serializer = RecommendationSerializer(recommendations, many=True)
        return Response({"results": serializer.data})
