import django_filters
from api.models import Evento


class Eventoilter(django_filters.FilterSet):
    class Meta:
        model = Evento
        fields = ['android_id', 'tipo', 'info', ]
