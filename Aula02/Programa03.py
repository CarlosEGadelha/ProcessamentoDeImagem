from asyncio import events
from cgitb import text
from fileinput import filename
from inspect import formatannotation
import io 
import os
from re import I
from tkinter import Button
from turtle import window_width
from urllib import request
import PySimpleGUI as sg
from PIL import Image
from pickletools import optimize

def main():
    layout = [
        [sg.Image(key="-IMAGE-", size=(500,500))],
        [
            sg.Text("Arquivo de imagem"),
            sg.Input(size=(25,1), key="-FILE-"),
            sg.FileBrowse(file_types=[("JPEG (*.jpg)", "*.jpg"), ("Todos os arquivos", "*.*")]),
            sg.Text("LINK da imagem"),
            sg.Input(size=(25,1), key="-LINK-"),
            sg.Button("Carregar imagem"),
            sg.Button("Tipo")
        ],
        [
            sg.Text("SALVAR COMO: "),
            sg.Input(size=(25,1), key="-SAVE-"),
            sg.Combo(["PNG","JPEG"], key="-FORMAT-"),
            sg.Button("Salvar"),
            sg.Button("Salvar Thumbnail"),
            sg.Button("Salvar Qualidade Reduzida")
        ]
    ]

    window = sg.Window("Visualizador de imagem", layout=layout)
    while True:
        event, value = window.read()
        if event == "Exit" or event == sg.WINDOW_CLOSED:
            break
        if event == "Carregar imagem":
            filename = value["-FILE-"]
            filelink = value["-LINK-"]
            if os.path.exists(filename):
                image = Image.open(filename)
                image.thumbnail((500,500))
                bio = io.BytesIO()
                image.save(bio, format="PNG")
                window["-IMAGE-"].update(data=bio.getvalue(), size = (500,500))
            else:
                image = Image.open(request.urlopen(filelink))
                image.thumbnail((500,500))
                bio = io.BytesIO()
                image.save(bio, format="PNG")
                window["-IMAGE-"].update(data=bio.getvalue(), size = (500,500))

        if event == "Salvar Thumbnail": 
            filename = value["-FILE-"]
            nome_img ="THUMBNAIL_" + filename.split("ProcessamentoImagem/",1)[1]
            print(filename)
            if os.path.exists(filename):
                image = Image.open(filename)    
                image.thumbnail([75,75])
                image.save(nome_img)

        if event == "Salvar Qualidade Reduzida":
            filename = value["-FILE-"]
            nome_img ="LQ_" + filename.split("ProcessamentoImagem/",1)[1]
            if os.path.exists(filename):
                image = Image.open(filename)
                image.save(nome_img, quality = 1)

        if event == "Salvar":
            filename = value["-FILE-"]
            formato = value["-FORMAT-"]
            new_filename =value["-SAVE-"] + "." + formato
            print(formato)

            image = Image.open(filename)
            image.save(new_filename, format=formato)

        if event == "Tipo":
            filename = value["-FILE-"]
            imagem = Image.open(filename)
            print(f"Formato: {imagem.format_description}")


    window.close()


if __name__ == "__main__":
    main()