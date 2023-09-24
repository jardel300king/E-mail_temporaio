import requests
import json
from time import sleep

lista_dominios = requests.get('https://www.1secmail.com/api/v1/?action=getDomainList').text
dominios = lista_dominios.replace('[', '').replace(']', '').replace('"', '').split(',')

def gera_mail(qt_mail=1): 
    qt_mail = str(qt_mail)
    url_base = (f'https://www.1secmail.com/api/v1/?action=genRandomMailbox&count={qt_mail}')
    response = requests.get(url_base)
    response = str(response.text).replace('[', '').replace(']', '').replace('"', '').split(',')
    return response[0]
    
#inicio
print(8*'=~~')
print('Gerando um E-mail.....')
print(8*'=~~')
email = gera_mail()
print(f'\nE-mail = {email}')

for indice, i in enumerate(dominios):
    if i in email:
        dominio = i
user = email.replace(dominio, '').replace('@','')
print('Aguardando mensagens.........')

def pegar_id(user, dominio):
    while True:
        respostas = requests.get(f'https://www.1secmail.com/api/v1/?action=getMessages&login={user}&domain={dominio}')
        respostas = str(respostas.text).replace('[','').replace(']','')
        if len(respostas) > 0:
            print(8*'=~~')
            print('E-mail detectado!')
            print(8*'=~~')
            dados = json.loads(respostas)
            idmail = dados['id']
            return idmail
        sleep(2)

id_mail = pegar_id(user=user,dominio=dominio)

texto_mensagem = requests.get(f'https://www.1secmail.com/api/v1/?action=readMessage&login={user}&domain={dominio}&id={id_mail}')
dados = json.loads(texto_mensagem.text)
print()
print(dados['textBody'])
print()
input('PRECIONE ENTER PARA FECHAR O PROGRAMA')