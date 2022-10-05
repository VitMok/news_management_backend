from rest_framework import serializers

from .models import (
    News,
)


class AmountNewsSerializer(serializers.Serializer):
    """ Сериализатор ввода количество новостей
    яндекса и озона, которое необходимо спарсить """
    amount_yandex_news = serializers.IntegerField(
        min_value=0
    )
    amount_ozon_news = serializers.IntegerField(
        min_value=0
    )

class NewsSerializer(serializers.ModelSerializer):
    """ Сериализатор новости """
    resource = serializers.SlugRelatedField(read_only=True, slug_field='name')
    tags = serializers.SlugRelatedField(read_only=True, slug_field='name', many=True)

    class Meta:
        model = News
        fields = '__all__'