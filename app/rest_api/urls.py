from django.urls import path, include
from rest_framework.routers import DefaultRouter

from rest_api.views import PollViewSet, AnswerViewSet

router = DefaultRouter()
router.register(r'polls', PollViewSet)
router.register(r'answers', AnswerViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
