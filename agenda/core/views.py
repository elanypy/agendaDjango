from django.shortcuts import render, HttpResponse, redirect
from core.models import Evento

# Create your views here.
def hello(request): #solicitação hello world
    return HttpResponse('Olá!')

def lista_eventos(request): #utilizando uma page em html para retornar a solicitação do user
    usuario = request.user
    evento =Evento.objects.filter(usuario=usuario)
    dados = {'eventos':evento}
    return render(request, 'agenda.html', dados)

def paginaTeste(request):
    return render(request, 'helloworld.html')

#redireciona para página Agenda sempre que o user não setar uma página específica. Uma das formas de fazer.
#def index(request):
#    return redirect('/agenda/')