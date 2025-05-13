import django_filters
from django.db.models import Q
from .models import RealEstate

class RealEstateFilter(django_filters.FilterSet):
    # id = django_filters.CharFilter(lookup_expr='iexact')
    city = django_filters.CharFilter(lookup_expr='iexact')
    # region = django_filters.filters.CharFilter(field_name='town', lookup_expr='icontains')
    # type = django_filters.CharFilter(lookup_expr='iexact')
    # minprice = django_filters.filters.NumberFilter(field_name='price', lookup_expr='gte')
    # maxprice = django_filters.filters.NumberFilter(field_name='price', lookup_expr='lte')
    # search = django_filters.CharFilter(method='filter_search')
    #
    class Meta:
        model = RealEstate
        fields = ['city',
                  # 'id'
                  # , 'region', 'type', 'minprice', 'maxprice', 'search'
                  ]

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     # Print the parameters being passed
    #
    # def filter_search(self, queryset, name, value):
    #     # Use Q objects to filter both `id` and `name` fields
    #     return queryset.filter(Q(id__iexact=value) | Q(town__icontains=value) |  Q(city__icontains=value))
