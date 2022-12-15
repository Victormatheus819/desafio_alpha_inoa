from django.db import models
from .timer import cycleRequisition
# Create your models here.
class Ativos (models.Model):
    nome= models.CharField(max_length=60,null=True)
    sigla=  models.CharField(max_length=60)
    preco_max= models.FloatField()
    preco_min = models.FloatField()
    cotacao = models.FloatField(null=True)
    search_interval=models.FloatField()
    cycleRequisition= cycleRequisition

class Usuario (models.Model):
    nome= models.CharField(max_length=60)
    email= models.CharField(max_length=60)