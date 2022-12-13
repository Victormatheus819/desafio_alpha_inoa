from django import views
from django.urls import path
from .views import *
urlpatterns=[
    path('novo-ativo/',create_new_ativo, name='novo_ativo')
]