
from django.shortcuts import render
from .forms import AtivosForm
from .models import Ativos
import requests
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from .timer import cycleRequisition
# Create your views here.
def home(request):
    ativos=Ativos.objects.all()
    return render(request,'home.html',{"ativos":ativos})

def create_user(request):
   user = User.objects.create_user(request.POST)
   if user.is_valid:
     user.save() 
     return render(request,'home.html',{"user":user})
   return render(request,'create_user.html')

def create_new_ativo(request):
    ativo= AtivosForm(request.POST)
    if ativo.is_valid():
        sigla=request.POST.get('sigla',False)
        search_interval=request.POST.get('search_interval',False)
        modelAtivo=Ativos.objects.filter(sigla=sigla)
        if len(modelAtivo) == 0:
             ativo.save()
             busca_valor_cotacao(sigla)
             return HttpResponseRedirect(reverse('index'))
        else:
             return render(request,'ativo_form.html',{"message":f'Ativo {sigla} já  existente em sua conta'})    
    return render(request,'ativo_form.html', {'form': ativo})

def delete_ativo(request, id):
  ativo = Ativos.objects.get(sigla=id)
  ativo.switch_off_thread=True
  ativo.save()
  return HttpResponseRedirect(reverse('index'))

def update_ativo(request, id):
    ativo = Ativos.objects.get(sigla=id)
    if request.POST.get('preco_max',0)!=0:
        ativo.preco_max=request.POST.get('preco_max',False)
        ativo.preco_min=request.POST.get('preco_min',False)
        ativo.search_interval=request.POST.get('search_interval',False)
        ativo.save()
        return HttpResponseRedirect(reverse('index'))
    
    return render(request,'update_ativo.html',{'ativo': ativo})
    
def busca_valor_cotacao(sigla):
    url = f'https://brapi.dev/api/quote/{sigla}'
    r = requests.get(url)
    ativo=Ativos.objects.get(sigla=sigla)
    
    
    data = r.json()
    cotacao=data['results'][0]['regularMarketPrice']
    ativo.nome=data['results'][0]['longName'] 
    ativo.cotacao=cotacao
    ativo.save()   
    if(ativo.preco_max<=cotacao):
        preco_superior()
    print(ativo.search_interval) 
    if(ativo.preco_min>=cotacao):
        preco_inferior()    
    requisicao = cycleRequisition(ativo.search_interval*60,busca_valor_cotacao,args=(sigla,))
    requisicao.start()
    if ativo.switch_off_thread == True:
        print("Desligando a thread ")
        requisicao.cancel()
        ativo.delete()
        return HttpResponseRedirect(reverse('index'))

def preco_superior():
    print("valor superior")   

def preco_inferior():
    print("valor inferior")    