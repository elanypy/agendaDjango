from django.shortcuts import render, HttpResponse, redirect
from core.models import Evento
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from datetime import datetime, timedelta
from django.http.response import Http404, JsonResponse



# Create your views here.
def hello(request): #solicitação hello world
    return HttpResponse('Olá!')

def loginUser(request):
    return render(request, 'login.html')

def logoutUser(request):
    logout(request)  #limpa a sessão
    return redirect('/') #redireciona para o index

def submitLogin(request):
    if request.POST:
        username = request.POST.get('username') #aqui eu obtenho do form no arquivo html login os dados do input (username e password)
        password = request.POST.get('password')

        usuario = authenticate(username=username, password=password)
        if usuario is not None:
            login(request, usuario)
            return redirect('/')
        else: #caso o  sistema nao conseguir autenticar, aparecerá uma mensagem de erro
            messages.error(request, 'Usuário ou senha inválidos')
    return redirect('/')

@login_required(login_url='/login/')
def submitEvento(request):
    if request.POST:
        titulo = request.POST.get('titulo')
        #local = request.POST.get('local')
        data_evento = request.POST.get('data_evento')
        descricao = request.POST.get('descricao')
        usuario = request.user
        id_evento = request.POST.get('id_evento')

        #caso exista um id de evento (em casos de editar)
        if id_evento:
            evento = Evento.objects.get(id=id_evento)
            if evento.usuario == usuario: #validando o usuario para verificar se o usuario que está alterando o evento é realmente dono do evento
                evento.titulo = titulo
                evento.descricao = descricao
                evento.data_evento = data_evento
                evento.save() #para commitar as alterações

            #segunda forma de atualizar as informações
            # Evento.objects.filter(id=id_evento).update(titulo = titulo,
            #                                             data_evento = data_evento,
            #                                             descricao = descricao)
        else:
            Evento.objects.create( titulo=titulo,
                                  # local=local,
                                   data_evento=data_evento,
                                   descricao=descricao,
                                   usuario=usuario)

    return redirect('/')

#adicionar evento / alterar evento
@login_required(login_url='/login/')
def evento(request):
    id_evento = request.GET.get('id')
    dados = {}
    if id_evento:
        dados['evento'] = Evento.objects.get(id=id_evento)
    return render(request, 'evento.html', dados)

@login_required(login_url='/login/')
def deleteEvento(request, id_evento):
    #validação para que cada usuário poderá deletar apenas seus eventos na agenda.
    usuario = request.user
    try:
            evento = Evento.objects.get(id=id_evento)
    except Exception:
        raise Http404()
    if usuario == evento.usuario:
        evento.delete()
    else:
        raise Http404()
    return redirect('/')

@login_required(login_url='/login/')  #exige a autenticação do usuário para poder acessar a agenda
def lista_eventos(request): #utilizando uma page em html para retornar a solicitação do user
    usuario = request.user
    data_atual = datetime.now() - timedelta(hours=1)
    evento =Evento.objects.filter(usuario=usuario,
                                  data_evento__gt= data_atual)   #nesse campo verifica a data o evento cadastrado
                                                                 #para saber se é maior (__gt) do que a data atual
                                                                 # para django não há possiblidade de colocar > e sim
                                                                 #__gt
    dados = {'eventos':evento}
    return render(request, 'agenda.html', dados)

def paginaTeste(request):
    return render(request, 'helloworld.html')

@login_required(login_url='/login/')
def json_lista_evento(request):
    usuario = request.user
    evento = Evento.objects.filter(usuario=usuario).values('id', 'titulo')
    return JsonResponse(list(evento), safe=False)



#redireciona para página Agenda sempre que o user não setar uma página específica. Uma das formas de fazer.
#def index(request):
#    return redirect('/agenda/')