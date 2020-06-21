import django_filters
from django_filters import DateFilter
from .models import *

class OrderFilter(django_filters.FilterSet):
    start_date = DateFilter(field_name="date_created",lookup_expr='Start')
    end_date = DateFilter(field_name="date_created",lookup_expr='End')

    class Meta:
        model = Order
        fields = '__all__' # means all fields allows
        exclude = ['customer','date_created'] 