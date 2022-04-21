import django_filters

from django.db.models.query_utils import Q

from .models import Contact


class ContactFilter(django_filters.FilterSet):
    search_query = django_filters.CharFilter(method='wide_filter', label="Search")
    first_name = django_filters.CharFilter(lookup_expr='icontains')
    middle_name = django_filters.CharFilter(lookup_expr='icontains')
    last_name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Contact
        fields = ['first_name', 'middle_name', 'last_name']

    def wide_filter(self, queryset, name, value):
        return queryset.filter(
            Q(first_name__icontains=value) | Q(
                middle_name__icontains=value) | Q(last_name__icontains=value)
        )
