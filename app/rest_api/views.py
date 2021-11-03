from django.utils import timezone
from rest_framework import viewsets

from polls.models import Poll
from rest_api.serializers import PollListSerializer, PollDetailSerializer


class PollViewSet(viewsets.ModelViewSet):
    today = timezone.localtime(timezone.now()).date()

    queryset = Poll.objects.filter(pub_date__lte=today, expiry_date__gte=today)
    serializer_class = PollDetailSerializer

    def get_serializer_class(self):
        if self.action in ('list',):
            return PollListSerializer
        return super().get_serializer_class()  # for create/destroy/update
