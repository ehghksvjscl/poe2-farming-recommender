from django.urls import path

from app.views import ContentPreferenceAPIView, RecommendationAPIView

urlpatterns = [
    path("recommendations/", RecommendationAPIView.as_view(), name="recommendations"),
    path("content-preferences/", ContentPreferenceAPIView.as_view(), name="content-preferences"),
]
