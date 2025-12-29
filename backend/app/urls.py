from django.urls import path

from app.views import (
    ContentPreferenceAPIView,
    FarmingMethodDetailAPIView,
    FarmingMethodListAPIView,
    MarketItemListAPIView,
    RecommendationAPIView,
)

urlpatterns = [
    path("recommendations/", RecommendationAPIView.as_view(), name="recommendations"),
    path("content-preferences/", ContentPreferenceAPIView.as_view(), name="content-preferences"),
    path("market-items/", MarketItemListAPIView.as_view(), name="market-items"),
    path("farming-methods/", FarmingMethodListAPIView.as_view(), name="farming-methods"),
    path("farming-methods/<slug:slug>/", FarmingMethodDetailAPIView.as_view(), name="farming-method-detail"),
]
