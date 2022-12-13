from django.shortcuts import render
from .forms import AtivosForm
from .models import Ativos
# Create your views here.
def home(request):
    ativos=Ativos.objects.all()
    return render(request,'home.html',{"ativos":ativos})


def create_new_ativo(request):
    ativo= AtivosForm(request.POST)
    sigla=request.POST['sigla']
    if ativo.is_valid():
        modelAtivo=Ativos.objects.filter(sigla=sigla)
        if len(modelAtivo) == 0:
            ativo.save()
            return render(request,'home.html')
        else:
             return render(request,'home.html',{"message":f'Ativo {sigla} já  existente em sua conta'})    
    return render(request,'ativo_form.html', {'form': ativo})


