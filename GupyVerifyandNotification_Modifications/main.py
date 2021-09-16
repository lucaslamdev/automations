from notify_run import Notify
from keep_alive import keep_alive
import bs4
import requests
import time

keep_alive()
urlIlegra = "https://ilegra.gupy.io/"
urlCompasso = "https://compasso.gupy.io/"

notificar = Notify(endpoint="https://notify.run/CODE")
print(notificar.info())

print('Olhando Ilegra')
htmlinteiroIlegra = requests.get(urlIlegra).text
soupIlegra = bs4.BeautifulSoup(htmlinteiroIlegra,'html.parser')
vagasIlegra = str(soupIlegra.find_all('div', class_="job-list"))

print('Olhando Compasso')
htmlinteiroCompasso = requests.get(urlCompasso).text
soupCompasso = bs4.BeautifulSoup(htmlinteiroCompasso,'html.parser')
vagasCompasso = str(soupCompasso.find_all('div', class_="job-list"))

while True:
    time.sleep(600)

    print('Verficando Novidades Ilegra')
    htmlinteiroIlegraNova = requests.get(urlIlegra).text
    soupIlegraNova = bs4.BeautifulSoup(htmlinteiroIlegraNova,'html.parser')
    vagasIlegraNova = str(soupIlegraNova.find_all('div', class_="job-list"))
    if vagasIlegra != vagasIlegraNova:
        try:
            vagasIlegra = vagasIlegraNova
            notificar.send('Vagas Novas Ilegra!', urlIlegra)
        except:
            print ('Algo de errado aconteceu...')

    print('Verficando Novidades Compasso')
    htmlinteiroCompassoNova = requests.get(urlCompasso).text
    soupCompassoNova = bs4.BeautifulSoup(htmlinteiroCompassoNova,'html.parser')
    vagasCompassoNova = str(soupCompassoNova.find_all('div', class_="job-list"))
    if vagasCompasso != vagasCompassoNova:
        try:
            vagasCompasso = vagasCompassoNova
            notificar.send('Vagas Novas Compasso!', urlCompasso)
        except:
            print ('Algo de errado aconteceu...')
