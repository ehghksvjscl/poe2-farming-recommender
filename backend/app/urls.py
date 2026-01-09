from django.urls import path, include
from rest_framework.routers import DefaultRouter

from app.views import HealthCheckView, KeywordViewSet, BlogPostViewSet, GeneratePostView

router = DefaultRouter()
router.register(r'keywords', KeywordViewSet)
router.register(r'posts', BlogPostViewSet)

urlpatterns = [
    path("health/", HealthCheckView.as_view(), name="health-check"),
    path("generate/", GeneratePostView.as_view(), name="generate-post"),
    path("", include(router.urls)),
]
