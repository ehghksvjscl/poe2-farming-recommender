from rest_framework.response import Response
from rest_framework.views import APIView


class HealthCheckView(APIView):
    """API 헬스체크 엔드포인트"""

    def get(self, request):
        return Response({"status": "ok", "message": "API is running"})


# 여기에 API 뷰를 추가하세요
# 예시:
# class ItemListView(APIView):
#     def get(self, request):
#         items = Item.objects.all()
#         serializer = ItemSerializer(items, many=True)
#         return Response({"items": serializer.data})
