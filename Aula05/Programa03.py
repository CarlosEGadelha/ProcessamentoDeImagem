from asyncio import events
from cgitb import text
from email.mime import image
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
from PIL.ExifTags import TAGS, GPSTAGS
from pathlib import Path
import os.path
from os import path

file_types = [("(JPEG (*.jpg)","*.jpg"),
              ("All files (*.*)", "*.*")]

fields = {
    "File name" : "File name",
    "File size" : "File size",
    "GPSLatitude" : "GPS Latitude",
    "GPSLongitude" : "GPS Longitude",
    "Model" : "Camera Model",
    "ExifImageWidth" : "Width",
    "ExifImageHeight" : "Height",
    "DateTime" : "Creating Date",
    "static_line" : "*",
    "MaxApertureValue" : "Aperture",
    "ExposureTime" : "Exposure",
    "FNumber" : "F-Stop",
    "Flash" : "Flash",
    "FocalLength" : "Focal Length",
    "ISOSpeedRatings" : "ISO",
    "ShutterSpeedValue" : "Shutter Speed"
}

def _get_if_exist(data, key):
    if key in data:
        return data[key]
    return None   

def carregar_imagem(filename, filelink, window):
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

def salvar_thumbnail(filename):
    if os.path.exists(filename):
        nome_img ="THUMBNAIL_" + filename.split("Aula04/",1)[1]    
        image = Image.open(filename)    

    image.thumbnail([75,75])
    image.save(nome_img)    


def salvar_qualidade_reduzida(filename):
    nome_img ="LQ_" + filename.split("Aula04/",1)[1]
    if os.path.exists(filename):
        image = Image.open(filename)
        image.save(nome_img, quality = 1)

def salvar(filename,formato, new_filename):
    print(formato)

    image = Image.open(filename)
    image.save(new_filename, format=formato)

def salvar_branco_preto(filename):
    nome_img ="PB_" + filename.split("Aula04/",1)[1]
    if os.path.exists(filename):
        image = Image.open(filename)
        image = image.convert("L")
        image.save(nome_img)

def calcula_paleta(branco):
    paleta = []
    r,g,b = branco
    for i in range(255):
        new_red = r * i // 255
        new_geen = g * i // 255
        new_blue = b * i // 255
        paleta.extend((new_red, new_blue, new_geen))
    return paleta    

def converte_sepia(filename):
    branco = (255, 240, 192)
    nome_img ="SEPIA_" + filename.split("Aula04/",1)[1]

    paleta = calcula_paleta(branco)

    imagem = Image.open(filename)
    imagem = imagem.convert("L")
    imagem.putpalette(paleta)
    sepia = imagem.convert("RGB")

    sepia.save(nome_img)   

def diminuir_cor(filename):
    nome_img ="CorDiminuida_" + filename.split("Aula04/",1)[1]
    imagem = Image.open(filename)
    imagem = imagem.convert("P", palette=Image.Palette.ADAPTIVE, colors = 6)
    imagem.save(nome_img)         

def get_exif_data(filename):
    exif_data = {}
    try:
        image = Image.open(filename)
        info = image._getexif()
    except OSError:
        info = {}

    #Se não encontrar o arquivo
    if info is None:
        info = {}
    for tag, value in info.items():
        decoded = TAGS.get(tag, tag)
        if decoded == "GPSInfo":
            gps_data = {}
            for gps_tag in value:
                sub_decoded = GPSTAGS.get(gps_tag, gps_tag)
                gps_data[sub_decoded] = value[gps_tag]
            exif_data[decoded] = gps_data
        else:
            exif_data[decoded] = value

    return exif_data

def main():
    menu_def = [['FILTROS', ['Thumbnail', 'Qualidade baixa', 'Preto e branco', 'Sepia', 'Diminuir cores']],
                ['INFOS', ["EXIF"]]]
    layout = [
        [
            sg.Menu(menu_def)
        ],

        [sg.Image(key="-IMAGE-", size=(500,500))],
        [
            sg.Text("LINK da imagem"),
            sg.Input(size=(25,1), key="-LINK-"),
            sg.Text("Arquivo de imagem"),
            sg.Input(size=(25,1), key="-FILE-"),
            sg.FileBrowse(file_types=[("JPEG (*.jpg)", "*.jpg"), ("Todos os arquivos", "*.*")]),
            sg.Button("Carregar imagem")
            #sg.Button("Tipo")
        ],
        [
            sg.Text("SALVAR COMO: "),
            sg.Input(size=(25,1), key="-SAVE-"),
            sg.Combo(["PNG","JPEG"], key="-FORMAT-"),
            sg.Button("Salvar")
        ]
    ]

    window = sg.Window("Visualizador de imagem", layout=layout)
    #exif_window = sg.Window("IMAGE INFO", exif_layout)
    
    while True:
        event, value = window.read()
        filename = Path(value["-FILE-"])
        #filename_Teste = Path(values["-LOAD-"])
        filelink = value["-LINK-"]
        formato = value["-FORMAT-"]
        new_filename = value["-SAVE-"] + "." + formato   

        if event == "Exit" or event == sg.WINDOW_CLOSED:
            break
        if event == "Carregar imagem":
            carregar_imagem(filename, filelink, window)

        if event == "Thumbnail":
            salvar_thumbnail(filename)

        if event == "Qualidade baixa":
            salvar_qualidade_reduzida(filename)

        if event == "Salvar":
            salvar(filename, formato, new_filename)

        if event == "Preto e branco":
            salvar_branco_preto(filename)    

        if event == "Sepia":
            converte_sepia(filename)

        if event == "Diminuir cores":
            diminuir_cor(filename)

        if event == "EXIF":
                
            exif_layout = [[ sg.FileBrowse("Load Image Data", file_types=file_types, key="-LOAD-", enable_events=True) ]]            

            for field in fields:
                exif_layout += [[sg.Text(fields[field], size=(10,1)),
                            sg.Text("", size=(25,1), key=field)]]

            exif_window = sg.Window("IMAGE INFO", exif_layout)
            
            while True:
                events, values = exif_window.read()

                if events == "Exit" or events == sg.WINDOW_CLOSED:
                    break
        
                #if events == "-LOAD-":
                image_path = Path(values["-LOAD-"])
                exif_data = get_exif_data(image_path.absolute())
                if "GPSInfo" in exif_data:
                    gps_info = exif_data["GPSInfo"]

                for field in fields:
                    if field == "File name":
                        exif_window[field].update(image_path.name)
                    elif field == "File size":
                        exif_window[field].update(image_path.stat().st_size)
                    elif field == "GPSLatitude":
                        exif_window[field].update(_get_if_exist(gps_info, "GPSLatitude"))
                    elif field == "GPSLongitude":
                        exif_window[field].update(_get_if_exist(gps_info, "GPSLongitude"))
                    else:
                        exif_window[field].update(exif_data.get(field, "No data"))   
                                        
        # if event == "Tipo":
        #     filename = value["-FILE-"]
        #     imagem = Image.open(filename)
        #     print(f"Formato: {imagem.format_description}")


    window.close()


if __name__ == "__main__":
    main()