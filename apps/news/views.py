from django.db import transaction
from rest_framework import viewsets, generics
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView

from .tasks import (
    parsing_news_from_yandex,
    parsing_news_from_ozon,
)
from .models import (
    News,
)
from .serializers import (
    NewsSerializer,
)
from .news_filtration import NewsFilter


class NewsParsingView(APIView):
    """ Парсинг новостей """

    @transaction.atomic
    def post(self, request):
        parsing_news_from_yandex.delay()
        parsing_news_from_ozon.delay()
        return Response({'message': 'Парсинг новостей запущен.'})

class NewsListView(generics.ListAPIView):
    """ Вывод списка новостей """
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = NewsFilter
