
from django.shortcuts import render
from .forms import AtivosForm
from .models import Ativos
import requests
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from .timer import cycleRequisition
from django.core.mail import send_mail
# Create your views here.
def home(request):
    ativos=Ativos.objects.all()
    return render(request,'home.html',{"ativos":ativos})

def create_user(request):
   email=request.POST.get('email',False)
   password=request.POST.get('password',False)
   username=request.POST.get('username',False)
   print(username)
   if username!=False:
    user = User.objects.create_user(email =email, username=username, password =password)
    user.save() 
    return HttpResponseRedirect(reverse('login'))
   return render(request,'create_user.html')

def create_new_ativo(request,):
    ativo= AtivosForm(request.POST)
    if ativo.is_valid():
        sigla=request.POST.get('sigla',False)
        if request.user.is_authenticated:
            email = request.user.email
        modelAtivo=Ativos.objects.filter(sigla=sigla)
        if len(modelAtivo) == 0:
             ativo.save()
             busca_valor_cotacao(sigla,email)
             return HttpResponseRedirect(reverse('index'))
        else:
             return render(request,'ativo_form.html',{"message":f'Ativo {sigla} já  existente em sua conta'})    
    return render(request,'ativo_form.html', {'form': ativo})

def delete_ativo(request, id):
  ativo = Ativos.objects.get(sigla=id)
  ativo.switch_off_thread=True
  ativo.delete()
  return HttpResponseRedirect(reverse('index'))

def update_ativo(request, id):
    ativo = Ativos.objects.get(sigla=id)
    if request.POST.get('preco_max',0)!=0:
        ativo.preco_max=request.POST.get('preco_max',False)
        ativo.preco_min=request.POST.get('preco_min',False)
        ativo.email_compra=False
        ativo.email_venda=False
        ativo.search_interval=request.POST.get('search_interval',False)
        ativo.save()
        return HttpResponseRedirect(reverse('index'))
    
    return render(request,'update_ativo.html',{'ativo': ativo})
    
def busca_valor_cotacao(sigla,email):
    url = f'https://brapi.dev/api/quote/{sigla}'
    r = requests.get(url)
    switch_off_thread=False
    try:
        ativo=Ativos.objects.get(sigla=sigla)
        print(email)
        data = r.json()
        cotacao=data['results'][0]['regularMarketPrice']
        ativo.nome=data['results'][0]['longName'] 
        ativo.cotacao=cotacao
        ativo.save()   
        if(ativo.preco_max<=cotacao and  ativo.email_venda== False):
            preco_superior(email,ativo)
        print(ativo.search_interval) 
        if(ativo.preco_min>=cotacao and ativo.email_compra==False):
            preco_inferior(email,ativo)
    except Ativos.DoesNotExist:            
        switch_off_thread=True
    requisicao = cycleRequisition(ativo.search_interval*60,busca_valor_cotacao,args=(sigla,email))
    requisicao.start()
    if switch_off_thread == True:
        print("finally")
        requisicao.cancel()
        ativo.delete()
        

def preco_superior(email,ativo):
    print("olha o email de venda")
    send_mail(
    'Oportunidade de venda',
    f'Hora de vender {ativo.sigla}',
    'from@example.com',
    [email],
    fail_silently=False,
)
    ativo.email_venda= True
    ativo.save() 

def preco_inferior(email,ativo):
    print("olha o email de compra")
    send_mail(
    'Oportunidade de compra',
    f'Hora de comprar {ativo.sigla}',
    'from@exa',
    [email],
    fail_silently=False,
)   
    ativo.email_compra= True
    ativo.save()