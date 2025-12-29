from django.urls import path

from app.views import RecommendationAPIView

urlpatterns = [
    path("recommendations/", RecommendationAPIView.as_view(), name="recommendations"),
]
