import requests
import json
from time import sleep
from colorama import just_fix_windows_console, Fore, Back, Style
just_fix_windows_console()
lista_ids = []

reset_cor = [Fore.RESET]
reset_fundo = [Back.RESET]
cores = {'azul':Fore.BLUE, 'cyan':Fore.CYAN, 'verde':Fore.GREEN, 'magenta':Fore.MAGENTA, 'vermelho':Fore.RED, 'amarelo':Fore.YELLOW,'branco':Fore.WHITE}
fundo = {'azul':Back.BLUE, 'cyan':Back.CYAN, 'verde':Back.GREEN, 'magenta':Back.MAGENTA, 'vermelho':Back.RED, 'amarelo':Back.YELLOW, 'branco':Back.WHITE}

lista_dominios = requests.get('https://www.1secmail.com/api/v1/?action=getDomainList').text
dominios = lista_dominios.replace('[', '').replace(']', '').replace('"', '').split(',')

def gera_mail(qt_mail=1): 
    qt_mail = str(qt_mail)
    url_base = (f'https://www.1secmail.com/api/v1/?action=genRandomMailbox&count={qt_mail}')
    response = requests.get(url_base)
    response = str(response.text).replace('[', '').replace(']', '').replace('"', '').split(',')
    return response[0]
    
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

def e_mail(user, dominio):
    cont = 0
    while True:
        respostas = requests.get(f'https://www.1secmail.com/api/v1/?action=getMessages&login={user}&domain={dominio}')
        
        if len(respostas.text) > 2:

            if cont == 0:
                print(8*'=~~')
                print('E-mail detectado!')
                print(8*'=~~')
                print()
                dados = json.loads(respostas.text)
                idmail = dados[0]['id']
                texto_mensagem = requests.get(f'https://www.1secmail.com/api/v1/?action=readMessage&login={user}&domain={dominio}&id={idmail}')
                texto = json.loads(texto_mensagem.text)
                print(10*'x=',end='')
                print(' INICIO')
                print(cores['verde'])
                print(texto['textBody'])
                print(reset_cor[0])
                print(10*'x=',end='')
                print(' FIM\n')
                lista_ids.append(idmail)
                cont+=1
                sleep(2)

            else:
                dados = json.loads(respostas.text)
                if dados[0]['id'] not in lista_ids:
                    print(8*'=~~')
                    print('E-mail detectado!')
                    print(8*'=~~')
                    print()
                    idmail = dados[0]['id']
                    texto_mensagem = requests.get(f'https://www.1secmail.com/api/v1/?action=readMessage&login={user}&domain={dominio}&id={idmail}')
                    texto = json.loads(texto_mensagem.text)
                    print(10*'x=',end='')
                    print(' INICIO')
                    print(cores['verde'])
                    print(texto['textBody'])
                    print(reset_cor[0])
                    print(10*'x=',end='')
                    print(' FIM\n')
                    lista_ids.append(idmail)
                    texto = json.loads(texto_mensagem.text)
                    sleep(2)

if __name__ == '__main__':
    id_mail = e_mail(user=user,dominio=dominio)


