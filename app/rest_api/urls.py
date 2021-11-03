from django.urls import path, include
from rest_framework.routers import DefaultRouter

from rest_api.views import PollViewSet, ReportView

router = DefaultRouter()
router.register(r'polls', PollViewSet)

urlpatterns = [
    path('report/', ReportView.as_view()),
    path('', include(router.urls)),
]
