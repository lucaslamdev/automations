import os
from PIL import Image

# fazer uma lista com todos os arquivos .png


def listaArquivos(caminho):
    lista = []
    for arquivo in os.listdir(caminho):
        if arquivo.endswith(".png"):
            lista.append(arquivo)
    return lista

# converter os arquivos .png para .pdf


def converter(lista, caminho):
    for arquivo in lista:
        img = Image.open(caminho + arquivo)
        img.save(caminho + arquivo[:-4] + ".pdf", "PDF", resolution=100.0)


def main():
    caminho = "./"
    lista = listaArquivos(caminho)
    converter(lista, caminho)


main()
