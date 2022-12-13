from django.db import models

# Create your models here.
class Ativos (models.Model):
    nome= models.CharField(max_length=60)
    sigla=  models.CharField(max_length=60)
    preco_max= models.FloatField()
    preco_min = models.FloatField()
    search_interval=models.FloatField()

class Usuario (models.Model):
    nome= models.CharField(max_length=60)
    email= models.CharField(max_length=60)