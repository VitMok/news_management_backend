from rest_framework import serializers

from .models import (
    News,
)


class NewsSerializer(serializers.ModelSerializer):
    """  """
    resource = serializers.SlugRelatedField(read_only=True, slug_field='name')
    tags = serializers.SlugRelatedField(read_only=True, slug_field='name', many=True)

    class Meta:
        model = News
        fields = '__all__'