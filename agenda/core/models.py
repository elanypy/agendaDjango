from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Evento(models.Model):
    titulo = models.CharField(max_length=100)
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
