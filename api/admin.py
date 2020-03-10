from django.contrib import admin
import math, datetime

from .models import Terminal, Evento, Info_pos, Incidente
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export.fields import Field
from .xls import ExcelDateWidget


class TerminalAdmin(admin.ModelAdmin):
    list_display = ('serie', 'mac', 'android_id', 'terminal')
    search_fields = ('serie', 'android_id', 'terminal',)


class IncidenteResource(resources.ModelResource):

    num_incidente = Field(attribute='id', column_name='TERM ID')
    reference = Field(attribute='reference', column_name='TICKET')
    assigned_party = Field(attribute='assigned_party', column_name='CAUSA RAIZ')
    status = Field(attribute='status', column_name='ESTADO TICKET')
    create_time = Field(attribute='create_time', column_name='FECHA INCIDENTE',
                        widget=ExcelDateWidget(dateformat="%Y-%m-%d %H:%M"))
    close_time = Field(attribute='close_time', column_name='FECHA CIERRE',
                       widget=ExcelDateWidget(dateformat="%Y-%m-%d %H:%M"))

    class Meta:
        model = Incidente
        import_id_fields = ('num_incidente',)
        exclude = ('id',)
        skip_unchanged = True
        report_skipped = False


class IncidenteAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'reference', 'status', 'assigned_party', 'create_time', 'close_time')
    search_fields = ('id', 'reference', 'status', 'assigned_party', 'create_time', 'close_time')
    resource_class = IncidenteResource


class InfoPosResource(resources.ModelResource):
    terminal = Field(attribute='terminal', column_name='TERM ID')
    nombre_comercio = Field(attribute='nombre_comercio', column_name='NOMBRE')
    nro_serie = Field(attribute='nro_serie', column_name='SERIE')
    estado = Field(attribute='estado', column_name='ESTADO')
    marca = Field(attribute='marca', column_name='MARCA')
    modelo = Field(attribute='modelo', column_name='MODELO')
    encargado = Field(attribute='encargado', column_name='ENCARGADO')
    direccion = Field(attribute='direccion', column_name='DIRECCION')
    distrito = Field(attribute='distrito', column_name='DISTRITO')
    provincia = Field(attribute='provincia', column_name='PROVINCIA')
    departamento = Field(attribute='departamento', column_name='DEPARTAMENTO')
    lp = Field(attribute='lp', column_name='LP')
    proveedor_enlace = Field(attribute='proveedor_enlace', column_name='PROVEDOR ENLACE')
    funcionalidad = Field(attribute='funcionalidad', column_name='FUNCIONALIDAD')
    ruta = Field(attribute='ruta', column_name='RUTA')
    nro_contacto = Field(attribute='nro_contacto', column_name='CONTACTO')
    grupo = Field(attribute='grupo', column_name='GRUPO')
    contacto_ruc = Field(attribute='contacto_ruc', column_name='CONTACTO RUC')

    class Meta:
        model = Info_pos
        import_id_fields = ('terminal',)
        exclude = ('id', 'monitoreado')
        skip_unchanged = True
        report_skipped = False
        
        
class InfoPosAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('terminal', 'nombre_comercio', 'nro_serie', 'estado', 'monitoreado', 'marca', 'modelo', 'encargado', 'direccion', 'distrito', 'provincia', 'departamento', 'lp', 'proveedor_enlace',
                    'funcionalidad', 'ruta', 'nro_contacto', 'grupo', 'contacto_ruc')
    search_fields = ('terminal', 'nombre_comercio', 'nro_serie', 'estado', 'marca', 'modelo', 'encargado', 'direccion', 'distrito', 'provincia', 'departamento', 'lp', 'proveedor_enlace',
                    'funcionalidad', 'ruta', 'nro_contacto', 'grupo', 'contacto_ruc')
    resource_class = InfoPosResource


admin.site.register(Terminal, TerminalAdmin)
admin.site.register(Evento)
admin.site.register(Info_pos, InfoPosAdmin)
admin.site.register(Incidente, IncidenteAdmin)
