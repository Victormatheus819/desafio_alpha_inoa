
from django.shortcuts import render
from .forms import AtivosForm
from .models import Ativos
import requests
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from .timer import cycleRequisition
from .threading_dict import thread_dictionary
from django.core.mail import send_mail
# Create your views here.
req__dictionary=thread_dictionary()
def home(request):
    ativos=Ativos.objects.all()
    return render(request,'home.html',{"ativos":ativos})
from django.contrib.auth import logout as auth_logout

def logout_custom(request):
    auth_logout(request)
    return render(request,"logged_out.html");
def create_user(request):
   email=request.POST.get('email',False)
   password=request.POST.get('password',False)
   username=request.POST.get('username',False)
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
             busca_valor_cotacao_inicial(sigla,email)
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
    
def busca_valor_cotacao_inicial(sigla,email):
    url = f'https://brapi.dev/api/quote/{sigla}'
    r = requests.get(url)
    ativo=Ativos.objects.get(sigla=sigla)
    data = r.json()
    cotacao=data['results'][0]['regularMarketPrice']
    ativo.nome=data['results'][0]['longName'] 
    ativo.cotacao=cotacao
    ativo.sigla=data['results'][0]['symbol'] 
    ativo.save()   
    if(ativo.preco_max<=cotacao and  ativo.email_venda== False):
        preco_superior(email,ativo)
    if(ativo.preco_min>=cotacao and ativo.email_compra==False):
        preco_inferior(email,ativo)            
    requisicao = cycleRequisition(ativo.search_interval*60,busca_valor_cotacao,args=(sigla ,email))
    req__dictionary.add(sigla,requisicao)
    requisicao.start()
   
def busca_valor_cotacao(sigla,email):
    url = f'https://brapi.dev/api/quote/{sigla}'
    r = requests.get(url)
    print(sigla)
    try:
        ativo=Ativos.objects.get(sigla=sigla)
        data = r.json()
        cotacao=data['results'][0]['regularMarketPrice']
        ativo.nome=data['results'][0]['longName'] 
        ativo.cotacao=cotacao
        ativo.sigla=data['results'][0]['symbol'] 
        ativo.save()   
        if(ativo.preco_max<=cotacao and  ativo.email_venda== False):
            preco_superior(email,ativo)
        if(ativo.preco_min>=cotacao and ativo.email_compra==False):
            preco_inferior(email,ativo)
    except Ativos.DoesNotExist:            
         req__dictionary[sigla].cancel()
         del req__dictionary[sigla]

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