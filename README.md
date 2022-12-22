# Desafio_alpha_inoa 
## Executado por Victor Matheus Pereira de Azevedo
Informações sobre a sobre a aplicação:\
Python:3.9\
Django: 3.2


## Passos para a execução da aplicação:

 1.Crie um ambiente virtual python ex:
 ````
 py -m venv <nome_do_seu ambiente_virtual>
````
2.Ative seu  ambiente virtual python:
````
<nome_do_seu ambiente_virtual>/Scripts/activate
````
3.Entre na pasta desafioAlpha:
````
cd desafioAlpha
````
4.Baixe as bibliotecas do pyhton:
````
 pip install -r requirements.txt
 ````
5.Execute  o comando :
````
 python manage.py migrate
 ````
6. crie o arquivo **.env** abaixo do settings.py , para conseguir enviar os emails: 
````
.env
EMAIL_HOST=<host_de_email>
EMAIL_HOST_USER=<endereco_de_email>
EMAIL_HOST_PASSWORD=<senha_do_aplicativo_de_email>

````
7.Execute o comando:
````
python manage.py runserver
````

8.Acesse a url em seu navegador:  
[http://127.0.0.1:8000/](http://127.0.0.1:8000/)
