from django.db import models
from django.utils import timezone


class Terminal(models.Model):
    id_terminal = models.AutoField(primary_key=True)
    serie = models.CharField(max_length=10)
    mac = models.CharField(max_length=17)
    android_id = models.CharField(max_length=16)
    terminal = models.CharField(max_length=10)  # BV00001234

    def __str__(self):
        return self.android_id


class Evento(models.Model):
    id_evento = models.AutoField(primary_key=True)
    android_id = models.CharField(max_length=16)
    timestamp = models.DateTimeField(auto_now_add=True)
    tipo = models.CharField(max_length=3)
    info = models.TextField()
    terminal = models.CharField(max_length=8)   # 00001234

    def __str__(self):
        timestamp = timezone.localtime(self.timestamp)
        return "["+timestamp.strftime('%Y-%m-%d %H:%M')+"] "+self.android_id + "-" + self.tipo
    
    
class Info_pos(models.Model):
    terminal = models.CharField(max_length=20)
    nombre_comercio = models.CharField(max_length=100)
    nro_serie = models.CharField(max_length=20, blank=True)
    estado = models.CharField(max_length=10)
    monitoreado = models.BooleanField(default=False)
    marca = models.CharField(max_length=20)
    modelo = models.CharField(max_length=20)
    encargado = models.CharField(max_length=100)
    direccion = models.CharField(max_length=300)
    distrito = models.CharField(max_length=50, blank=True)
    provincia = models.CharField(max_length=30)
    departamento = models.CharField(max_length=30)
    lp = models.CharField(max_length=20)
    proveedor_enlace = models.CharField(max_length=20)
    funcionalidad = models.CharField(max_length=30)
    ruta = models.CharField(max_length=20)
    nro_contacto = models.CharField(max_length=120)
    grupo = models.CharField(max_length=20)
    contacto_ruc = models.CharField(max_length=11)

    class Meta:
        verbose_name = "Información del POS"
        verbose_name_plural = "Información de los POS"


class Incidente(models.Model):
    num_incidente = models.BigIntegerField(null=True)
    reference = models.CharField(max_length=8)
    status = models.CharField(max_length=5)
    create_time = models.DateTimeField()
    assigned_party = models.CharField(max_length=12)
    close_time = models.DateTimeField(null=True)


class Disponibilidad(models.Model):
    dia = models.DateField(auto_now_add=True)
    porcentaje_de_disponibilidad = models.FloatField()
    operativos = models.IntegerField()
    inoperativos = models.IntegerField()
    ids_intervalo_1 = models.IntegerField()
    ids_intervalo_2 = models.IntegerField()
    ids_intervalo_3 = models.IntegerField()
