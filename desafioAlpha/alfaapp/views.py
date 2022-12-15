from django.shortcuts import render
from .forms import AtivosForm
from .models import Ativos
from threading import Thread
import requests
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
import schedule
from .timer import cycleRequisition
# Create your views here.
def home(request):
    ativos=Ativos.objects.all()
    return render(request,'home.html',{"ativos":ativos})


def create_new_ativo(request):
    ativo= AtivosForm(request.POST)
    if ativo.is_valid():
        sigla=request.POST.get('sigla',False)
        search_interval=request.POST.get('search_interval',False)
        modelAtivo=Ativos.objects.filter(sigla=sigla)
        if len(modelAtivo) == 0:
            ativo.save()
            requisicao=cycleRequisition(search_interval,busca_valor_cotacao(sigla))
            requisicao.start()
            
            return HttpResponseRedirect(reverse('index'))
        else:
             return render(request,'ativo_form.html',{"message":f'Ativo {sigla} já  existente em sua conta'})    
    return render(request,'ativo_form.html', {'form': ativo})

def delete_ativo(request, id):
  ativo = Ativos.objects.get(sigla=id)
  ativo.delete()
  return HttpResponseRedirect(reverse('index'))

def update_ativo(request, id):
    ativo = Ativos.objects.get(sigla=id)
    print(request.POST.get('preco_max',0))
    if request.POST.get('preco_max',0)!=0:
        ativo.preco_max=request.POST.get('preco_max',False)
        ativo.preco_min=request.POST.get('preco_min',False)
        ativo.search_interval=request.POST.get('search_interval',False)
        ativo.save()
        return HttpResponseRedirect(reverse('index'))
    print(request.POST)
    return render(request,'update_ativo.html',{'ativo': ativo})
    



def busca_valor_cotacao(sigla):
    
    url = f'https://brapi.dev/api/quote/{sigla}'
    r = requests.get(url)
    ativo=Ativos.objects.get(sigla=sigla)
    data = r.json() 
    print(data)
    ativo.nome=data['results'][0]['longName'] 
    ativo.cotacao=data['results'][0]['regularMarketPrice']
    ativo.save()
    
    