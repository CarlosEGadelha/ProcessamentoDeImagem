from asyncio import events
from cgitb import text
from fileinput import filename
import io 
import os
from turtle import window_width
import PySimpleGUI as sg
from PIL import Image

def main():
    layout = [
        [sg.Image(key="-IMAGE-", size=(500,500))],
        [
            sg.Text("Arquivo de imagem"),
            sg.Input(size=(25,1), key="-FILE-"),
            sg.FileBrowse(file_types=[("JPEG (*.jpg)", "*.jpg"), ("Todos os arquivos", "*.*")]),
            sg.Button("Carregar imagem")
        ]
    ]

    window = sg.Window("Visualizador de imagem", layout=layout)
    while True:
        event, value = window.read()
        if event == "Exit" or event == sg.WINDOW_CLOSED:
            break
        if event == "Carregar imagem":
            filename = value["-FILE-"]
            if os.path.exists(filename):
                image = Image.open(filename)
                image.thumbnail((500,500))
                bio = io.BytesIO()
                image.save(bio, format="PNG")
                window["-IMAGE-"].update(data=bio.getvalue(), size = (500,500))
    window.close()


if __name__ == "__main__":
    main()