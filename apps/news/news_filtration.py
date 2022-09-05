from django_filters import rest_framework as filters

from .models import News


class CharFilterInFilter(filters.BaseInFilter, filters.CharFilter):
    pass

class NewsFilter(filters.FilterSet):
    resource = filters.CharFilter(field_name='resource__name')
    tags = CharFilterInFilter(field_name='tags__name', lookup_expr='in')

    class Meta:
        model = News
        fields = ['resource', 'tags', 'date']