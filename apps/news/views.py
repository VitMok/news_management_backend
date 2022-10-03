from django.db import transaction, connection
from rest_framework import viewsets, generics, status
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
    AmountNewsSerializer,
    NewsSerializer,
)
from .news_filtration import NewsFilter


class NewsParsingView(generics.ListCreateAPIView):
    """  """
    serializer_class = AmountNewsSerializer

    def list(self, request, *args, **kwargs):
        return Response({'message': 'Введите количество новостей, которое необходимо спарсить.'})

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer_class()(data=request.data)
        if serializer.is_valid():
            cursor = connection.cursor()
            cursor.execute("TRUNCATE TABLE news RESTART IDENTITY CASCADE")
            parsing_news_from_yandex.delay(serializer.data['amount_yandex_news'])
            parsing_news_from_ozon.delay(serializer.data['amount_ozon_news'])
            return Response({'message': 'Парсинг новостей запущен.'})
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class NewsParsingView(APIView):
#     """ Парсинг новостей """
#
#     @transaction.atomic
#     def post(self, request):
#         parsing_news_from_yandex.delay()
#         parsing_news_from_ozon.delay()
#         return Response({'message': 'Парсинг новостей запущен.'})

class NewsListView(generics.ListAPIView):
    """ Вывод списка новостей """
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = NewsFilter
