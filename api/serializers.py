from rest_framework import serializers
from .models import Terminal, Evento


class TerminalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Terminal
        fields = ('android_id', 'terminal', 'mac', 'serie')
        
    def create(self, validate_data):
        return Terminal.objects.create(**validate_data)


class EventoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Evento
        fields = ('android_id', 'tipo', 'info', 'terminal')

    def create(self, validate_data):
        return Evento.objects.create(**validate_data)
