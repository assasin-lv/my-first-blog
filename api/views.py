import datetime
import itertools

from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.forms import model_to_dict
from django.http import HttpResponse
from django.db.models import Q
from django.shortcuts import render, redirect
from django.utils import timezone
from django_tables2 import RequestConfig
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets, generics, status

from api.tables import EventoTable, TerminalTable
from .models import Terminal, Evento, Info_pos, Disponibilidad
from .serializers import TerminalSerializer, EventoSerializer

from rest_framework.permissions import IsAuthenticated


class TerminalView(generics.ListAPIView):
    # permission_classes = (IsAuthenticated,)
    serializer_class = TerminalSerializer

    def get_queryset(self, *args, **kwargs):
        return Terminal.objects.filter(android_id=self.request.GET.get('android_id'))
    
    def post(self, request):
        try:
            terminal_seleccionado = Terminal.objects.get(android_id=request.data['android_id'])
            
        except Terminal.DoesNotExist:
            terminal_seleccionado = ''

        if terminal_seleccionado is not '':
            terminal_seleccionado.android_id = request.data['android_id']
            terminal_seleccionado.terminal = request.data['terminal']
            terminal_seleccionado.serie = request.data['serie']
            terminal_seleccionado.mac = request.data['mac']
            terminal_seleccionado.save()

            return Response(model_to_dict(terminal_seleccionado), status=status.HTTP_202_ACCEPTED)
        
        else:
            terminal = request.data
            
            serializer = TerminalSerializer(data=terminal)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        
            return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
    
    
class EventoView(APIView):

    def get(self, request):
        evento = Evento.objects.all()
        serializer = EventoSerializer(evento, many=True)
        return Response({"evento": serializer.data})

    def post(self, request):
        # TODO: agregar el dato de terminal al evento (se obviene con en android_id en la tabla Terminal)

        evento = request.data.get('evento')

        try:
            terminal = Terminal.objects.get(android_id = evento['android_id'])
        except Terminal.DoesNotExist:
            evento['terminal'] = '99999999'
        else:
            evento['terminal'] = terminal.terminal
        
        serializer = EventoSerializer(data=evento)
        
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            
        return Response({"success": "guardado"})


@login_required
def dashboard(request):
    ultimos_eventos = Evento.objects.raw("select id_evento, timestamp, nro_serie, nombre_comercio, tipo "
                                         "from api_evento a left join api_info_pos b on a.android_id = b.terminal "
                                         "order by timestamp desc limit 20")
    
    equipos_count = Terminal.objects.count()
    eventos_hoy_count = Evento.objects.filter(timestamp__date=datetime.date.today()).count()
    eventos_count = Evento.objects.count()

    # https://stackoverflow.com/questions/17303194/django-group-by-id-then-select-max-timestamp
    equipos_con_log = Evento.objects.filter(timestamp__date=datetime.date.today()).values('android_id').distinct()
    periodo1 = timezone.now() - datetime.timedelta(minutes=5)
    count_periodo1 = equipos_con_log.filter(timestamp__gte=periodo1).count()
    periodo2 = timezone.now() - datetime.timedelta(minutes=15)
    count_periodo2 = equipos_con_log.filter(timestamp__gte=periodo2).count() - count_periodo1
    periodo3 = timezone.now() - datetime.timedelta(minutes=60)
    count_periodo3 = equipos_con_log.filter(timestamp__gte=periodo3).count() - count_periodo2 - count_periodo1
    
    count_total = count_periodo1 + count_periodo2 + count_periodo3
    context = {
        'ultimos_eventos': ultimos_eventos,
        'eventos_count': eventos_count,
        'equipos_count': equipos_count,
        'eventos_hoy': eventos_hoy_count,
        'count_periodo1': count_periodo1,
        'count_periodo2': count_periodo2,
        'count_periodo3': count_periodo3,
        'count_total': count_total,

    }
    return render(request, 'api/dashboard.html', context)


@login_required
def log(request):
    titulo = "Eventos"
    table = EventoTable(Evento.objects.all().order_by('-timestamp'))
    RequestConfig(request, paginate={'per_page': 15}).configure(table)
    return render(request, 'api/tabla.html', {'table': table, 'titulo': titulo})


@login_required
def inventario(request):
    titulo = "Inventario"
    table = TerminalTable(Terminal.objects.all())
    RequestConfig(request, paginate={'per_page': 15}).configure(table)
    return render(request, 'api/tabla.html', {'table': table, 'titulo': titulo})


@login_required
def hoy(request):
    titulo = "Eventos del día"
    from django.utils import timezone
    t = timezone.localtime(timezone.now())
    eventos = Evento.objects.filter(timestamp__year=t.year, timestamp__month=t.month, timestamp__day=t.day)\
        .order_by('-timestamp')

    # https://stackoverflow.com/questions/30465013/django-group-by-hour
    def date_hour(timestamp):
        return timezone.localtime(timestamp).strftime("%H:00")

    groups = itertools.groupby(eventos, lambda x: date_hour(x.timestamp))
    # since groups is an iterator and not a list you have not yet traversed the list
    eventos_por_hora = []
    for group, matches in groups:  # now you are traversing the list ...
        punto = {"x": group, "y": sum(1 for _ in matches)}
        eventos_por_hora.append(punto)

    table = EventoTable(eventos)
    RequestConfig(request, paginate={'per_page': 15}).configure(table)
    return render(request, 'api/hoy.html', {'table': table, 'titulo': titulo, 'eventos_por_hora': str(eventos_por_hora)})


@login_required
def reportes(request):
    titulo = "Reporte de Eventos"
    
    if request.method == 'POST':
        inicio = datetime.datetime.strptime(request.POST.get('datepicker_inicio'), '%m/%d/%Y')
        fin = datetime.datetime.strptime(request.POST.get('datepicker_fin'), '%m/%d/%Y')
        
        # from django.utils import timezone
        # t = timezone.localtime(timezone.now())
    
        if inicio == fin:
            print('iguales')
            eventos = Evento.objects.filter(timestamp = inicio)
        else:
            eventos = Evento.objects.filter(Q(timestamp__gte = inicio) & Q(timestamp__lte = fin)).order_by('-timestamp')
        
        if len(eventos) == 0:
            return render(request, 'api/reportes.html', {'titulo': titulo, 'message': 'No existen logs en el rango de fechas seleccionado.', 'inicio':inicio, 'fin': fin})
    
        # https://stackoverflow.com/questions/30465013/django-group-by-hour
        def date_hour(timestamp):
            return timezone.localtime(timestamp).strftime("%H:00")
    
        groups = itertools.groupby(eventos, lambda x: date_hour(x.timestamp))
        # since groups is an iterator and not a list you have not yet traversed the list
        eventos_por_hora = []
        for group, matches in groups:  # now you are traversing the list ...
            punto = {"x": group, "y": sum(1 for _ in matches)}
            eventos_por_hora.append(punto)
    
        table = EventoTable(eventos)
        RequestConfig(request, paginate={'per_page': 15}).configure(table)
        return render(request, 'api/reportes.html', {'table': table, 'titulo': titulo, 'eventos_por_hora': str(eventos_por_hora), 'inicio': inicio, 'fin': fin})
    
    else:
        return render(request, 'api/reportes.html', {'titulo': titulo})


@login_required
def info(request, android_id):
    return HttpResponse("Terminal: %s." % android_id)


def logout_view(request):
    logout(request)
    return redirect("dashboard")


@login_required
def productividad(request):
    from datetime import date
    today = date.today()

    equipos = Info_pos.objects.filter(estado='PRODUCCION')
    equipos_total = equipos.count()
    equipos_monitoreados = equipos.filter(monitoreado=True).count()
    equipos_sin_monitorear = equipos_total - equipos_monitoreados

    activos = Evento.objects.filter(timestamp__date=datetime.date.today()).values('android_id').distinct().count()
    inactivos = equipos_monitoreados - activos

    porcentaje_activos = activos * 100 / equipos_monitoreados

    context = {
        'hoy': today.strftime("%d/%m/%y"),
        'equipos_monitoreados': equipos_monitoreados,
        'equipos_sin_monitorear': equipos_sin_monitorear,
        'equipos_total': equipos_total,
        'activos': activos,
        'inactivos': inactivos,
        'total': equipos_monitoreados,
        'porcentaje_activos': porcentaje_activos,
    }
    return render(request, 'api/productividad.html', context)

@login_required
def disponibilidad(request):
    from datetime import date, timedelta
    yesterday = date.today() - timedelta(1)

    disponibilidad_ayer = Disponibilidad.objects.filter(dia=yesterday).get_or_create()[0]

    context = {
        'ayer': yesterday.strftime("%d/%m/%y"),
        'disponibilidad': disponibilidad_ayer.porcentaje_de_disponibilidad*100,
        'equipos_operativos': disponibilidad_ayer.operativos,
        'equipos_inoperativos': disponibilidad_ayer.inoperativos,
        'incidencias_1': disponibilidad_ayer.ids_intervalo_1,
        'incidencias_2': disponibilidad_ayer.ids_intervalo_2,
        'incidencias_3': disponibilidad_ayer.ids_intervalo_3,
    }

    return render(request, 'api/disponibilidad.html', context)

