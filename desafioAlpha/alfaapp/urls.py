from django import views
from django.urls import path
from .views import *
urlpatterns=[
    path('novo-ativo/',create_new_ativo, name='novo_ativo'),
    path('delete-ativo/<slug:id>',delete_ativo, name='delete_ativo'),
    path('update-ativo/<slug:id>',update_ativo, name='update_ativo'),
    path('create-user/',create_user, name='create_user')
]