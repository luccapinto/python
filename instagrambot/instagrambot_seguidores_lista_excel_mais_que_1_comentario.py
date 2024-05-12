"""
Esse bot irá pegar os seguidores da conta e fazer o comentário com esses seguidores (username)
em um post de sorteio do instagram

Flávio Oliviera - 2021
https://www.github.com/oliveiradeflavio
"""


#importação de lib
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.keys import Keys
import time
import random
from PySimpleGUI import PySimpleGUI as sg
from datetime import datetime
from selenium.webdriver.common.by import By

class instagramBot:
    def __init__(self, username, password, verificacaoCodigo):
        self.username = username
        self.password = password
        self.verificacaoCodigo = verificacaoCodigo
        service = Service(executable_path="/Users/tripa/Documents/GitHub/python_social_media/instagrambot/geckodriver.exe") #caminho de onde está a biblioteca geckodriver 
        self.driver = webdriver.Firefox(service=service)
    def login(self):
        driver = self.driver
        driver.get("https://www.instagram.com")
        #input[@name=username] = login inspecionado na pagina instagram
        #input[@name=password] = senha inspecionado na pagina instagram
        #input[@name=verificationCode] = verificaçao de codigo em autenticaçao de dois fatores
        time.sleep(3)
        campo_usuario = driver.find_element(By.XPATH, "//input[@name='username']")
        campo_usuario.click()
        campo_usuario.clear()
        campo_usuario.send_keys(self.username)
        campo_senha = driver.find_element(By.XPATH, "//input[@name='password']")
        campo_senha.clear()
        campo_senha.send_keys(self.password)
        campo_senha.send_keys(Keys.RETURN)
        time.sleep(10)
        pagina_verificacao = driver.find_element(By.XPATH, "//div[@class='_ap3a _aaco _aacu _aad6']")
        pagina_verificacao.click()
        pagina_verificacao.clear()
        time.sleep(3)
        campo_verificacao_codigo = driver.find_element(By.XPATH, "//input[@name='verificationCode']")
        campo_verificacao_codigo.click()
        campo_verificacao_codigo.clear()
        campo_verificacao_codigo.send_keys(self.verificacaoCodigo)
        campo_verificacao_codigo.send_keys(Keys.RETURN)
        time.sleep(3)
        self.comentar_no_sorteio()

    #digitando os comentário na velocidade humanos, as vezes acelerando as vezes um pouco mais lento.
    @staticmethod
    def digitando_como_humano(frase, onde_digitar):
        for letra in frase:
            onde_digitar.send_keys(letra)
            time.sleep(random.randint(1,5)/30)  
        
    def comentar_no_sorteio(self):
        driver = self.driver
        driver.get("https://www.instagram.com/p/C6uOcMayXJT")
        time.sleep(3)
        #curti o post do sorteio
        curtir_post = driver.find_element_by_xpath("//span[@class='_aamw']")
        curtir_post.click()
        print("Like")
        time.sleep(2)
        try:
            contador = 0
            #irá pegar os username do insta na lista do excel
            #a cada username dentro da lista, irá a ser publicado no post de sorteio.
            
            tamanho = len(self.lista_seguidores['username']) # para publicar 2 comentário ou mais mude a variavel 2 do range
            for i in range(0, 10): #nesse caso estamos publicando 2 comentários por vez
                time.sleep(5)      
                campo_comentario = driver.find_element_by_css_selector("[placeholder='Adicione um comentário...']")
                time.sleep(random.randint(2,5))
                #para comentar mais que 2 comentário, altere a variavel 2 do range(0, tamanho, 2) para o número de comentário que você deseja
                #adicione a quantidade correspondente ao número de comentários self.lista_seguidores['username'][perfil_seguidores+1] na função digitando_como_humano
                self.digitando_como_humano('@'+self.lista_seguidores["username"]["@_mucardoso"], campo_comentario)
                time.sleep(random.randint(10,20))
                campo_comentario.send_keys(Keys.RETURN)
                time.sleep(5)
                #quando o contador atingir o valor 50, o sistema irá pausar no comentário
                #e contador será zerado.A ssim tentamos evitar o bloqueio da conta. 
                contador = contador + 1
                print("Usernames Comentados: " + i)
                driver.refresh()
                if contador == 50:
                    contador = 0
                    print('Sistema em espera, voltará a comentar em 1 hora. Última pausa feita: ', datetime.now().hour,datetime.now().minute)
                    time.sleep(3600) #1 hora
            
            print("Comentarios Enviados. ", datetime.now().hour,datetime.now().minute)

        except Exception as e:
            print(e)
            time.sleep(5)

#Layout
sg.theme('Reddit')
layout = [
    [sg.Text('Username'),sg.Input(key='username', size=(30, 4))],
    [sg.Text('Password'),sg.Input(key='password',password_char='*', size=(30,4))],
    [sg.Text('Verificação 2 Fatores'),sg.Input(key='vefificacaoCodigo', size=(30,4))],
    [sg.Button('Logar')]
    #[sg.Output(size=(50,20))]
]

#Janela
janela = sg.Window('BOT INSTAGRAM SORTEIO LISTA EXCEL', layout)

#ler os eventos
while True:
    eventos, valores = janela.read()
    if eventos == sg.WINDOW_CLOSED:
        break
    if eventos == 'Logar':
        if valores['username'] == '' or valores['password'] == '' or valores['vefificacaoCodigo'] == '':
            sg.Popup('Há campos vazios a serem preenchidos', title='Atenção')
        else:
            flavioBot = instagramBot(valores['username'], valores['password'], valores['vefificacaoCodigo'] )
            flavioBot.login()