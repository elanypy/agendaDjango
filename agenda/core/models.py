from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.
class Evento(models.Model):
    titulo = models.CharField(max_length=100)
   # local = models.CharField(max_length = 200, blank=True, verbose_name='Local do Evento')
    descricao = models.TextField(blank=True)
    data_evento = models.DateTimeField(verbose_name='Data do Evento')
    data_criacao = models.DateTimeField(auto_now=True, verbose_name='Data da Criaçao') #auto_now = significa que sempre que foir criado um registro,
                                                        #pegará a hora atual
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta: #classe para trocar o nome da tabela para 'Evento'
        db_table = "Evento"

    def __str__(self):
        return self.titulo

    def get_data_evento(self): #muda o estilo de saida da data do evento
        return self.data_evento.strftime('%d/%m/%Y %H:%M')

    def get_data_input_evento(self):
        return self.data_evento.strftime('%Y-%m-%dT%H:%M') #padrão que vai estar no input

    #verifica se o evento cadastrado está atrasado
    def get_evento_atrasado(self):
        if self.data_evento < datetime.now():
            return True
        else:
            return False
