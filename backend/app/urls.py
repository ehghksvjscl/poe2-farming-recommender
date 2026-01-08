from django.urls import path

from app.views import HealthCheckView

urlpatterns = [
    path("health/", HealthCheckView.as_view(), name="health-check"),
    # 여기에 URL 패턴을 추가하세요
    # path("items/", ItemListView.as_view(), name="item-list"),
]
