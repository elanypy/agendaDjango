from django.shortcuts import render, HttpResponse, redirect
from core.models import Evento
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages


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


@login_required(login_url='/login/')  #exige a autenticação do usuário para poder acessar a agenda
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