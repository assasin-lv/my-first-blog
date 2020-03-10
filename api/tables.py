import django_tables2 as tables
from django_filters.views import FilterView
from django_tables2 import SingleTableMixin

from filters import Eventoilter
from .models import Evento, Terminal


class EventoTable(tables.Table):
    class Meta:
        model = Evento
        template_name = 'django_tables2/bootstrap4.html'


class TerminalTable(tables.Table):
    class Meta:
        model = Terminal
        template_name = 'django_tables2/bootstrap4.html'


class FilteredEventoListView(SingleTableMixin, FilterView):
    table_class = EventoTable
    model = Evento
    template_name = 'django_tables2/bootstrap4.html'

    filterset_class = Eventoilter