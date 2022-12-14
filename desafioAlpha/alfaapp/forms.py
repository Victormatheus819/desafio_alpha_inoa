from django.forms import ModelForm
from .models import Ativos


class AtivosForm(ModelForm):
    class Meta:
        model = Ativos
        fields = ['sigla','preco_max','preco_min','search_interval']