from django.db import transaction
from django.shortcuts import render
from rest_framework import viewsets, generics
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView

from .models import (
    News,
)
from .serializers import (
    CreateNewsSerializer,
    NewsSerializer,
)
from .services import (
    _parsing_news_from_yandex_and_ozon,
)
from .news_filtration import NewsFilter


class NewsParsingView(APIView):
    """ Парсинг новостей """

    @transaction.atomic
    def post(self, request):
        queryset = _parsing_news_from_yandex_and_ozon()
        serializer = CreateNewsSerializer(queryset, many=True)
        return Response(serializer.data)

class NewsListView(generics.ListAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = NewsFilter
