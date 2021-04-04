import pyautogui
from time import sleep

def clicar(x, y):
    pyautogui.moveTo(x, y)
    pyautogui.click()
    print('Cliquei')

def verificar_tela():
    posicaobotao = pyautogui.locateOnScreen('fila.png', confidence=0.7)
    if posicaobotao != None:
        clicar(posicaobotao.left, posicaobotao.top)
        print('Botao encontrado!')
        return True

def main():
    while True:
        if verificar_tela():
            sleep(5)

main()
