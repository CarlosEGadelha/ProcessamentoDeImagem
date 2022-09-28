from asyncio import events
from cgitb import text
from email.mime import image
from fileinput import filename
from inspect import formatannotation
import io 
import os
from re import I
from tkinter import Button
from tokenize import Double
from turtle import window_width
from urllib import request
import PySimpleGUI as sg
from PIL import Image
from pickletools import optimize
from PIL.ExifTags import TAGS, GPSTAGS
from pathlib import Path
import os.path
from os import path
import shutil
import tempfile
from PIL import ImageEnhance

def _get_if_exist(data, key):
    if key in data:
        return data[key]
    return None   

def atualizar_imagem(tmp_file, window):
    imagem_tmp = Image.open(tmp_file)
    imagem_tmp.thumbnail((400,400))
    bio = io.BytesIO()
    imagem_tmp.save(bio, format="PNG")
    window["-IMAGE-"].update(data=bio.getvalue(), size=(400, 400)) 

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

            

def salvar_thumbnail(filename, output):
    image = Image.open(filename)      
    image.thumbnail([75,75])
    new_image = image

    new_image.save(output)


def salvar_qualidade_reduzida(filename, output):
    if os.path.exists(filename):
        image = Image.open(filename)
        new_image = image
        new_image.save(output, quality = 1)

def salvar(filename,formato, new_filename):
    print(formato)

    image = Image.open(filename)
    image.save(new_filename, format=formato)

def salvar_branco_preto(filename, output):
    if os.path.exists(filename):
        image = Image.open(filename)
        image = image.convert("L")
        new_image = image
        new_image.save(output)       

def calcula_paleta(branco):
    paleta = []
    r,g,b = branco
    for i in range(255):
        new_red = r * i // 255
        new_geen = g * i // 255
        new_blue = b * i // 255
        paleta.extend((new_red, new_blue, new_geen))
    return paleta    

def converte_sepia(filename, output):
    branco = (255, 240, 192)

    paleta = calcula_paleta(branco)

    imagem = Image.open(filename)
    imagem = imagem.convert("L")
    imagem.putpalette(paleta)
    sepia = imagem.convert("RGB")
    new_image = sepia

    new_image.save(output)   

def diminuir_cor(filename, output):
    imagem = Image.open(filename)
    imagem.convert("L", palette=Image.Palette.ADAPTIVE, colors = 6)
    new_image = imagem
    new_image.save(output)         

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

def exif():
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

def mirror(filename, output):
    image = Image.open(filename)
    mirror_image = image.transpose(Image.FLIP_TOP_BOTTOM) #FLIP_LEFT_RIGHT, FLIP_TOP_BOTTOM, TRANSPOSE
    new_image = mirror_image
    new_image.save(output)

def crop_image(image_path, output_image_path):
    layout_recortar = [
        [sg.Graph(key="-IMAGE-", canvas_size=(500,500), graph_bottom_left=(0, 0), graph_top_right=(400, 400), change_submits=True, drag_submits=True)],
        [
            sg.Text("Arquivo de Imagem"),
            sg.Input(size=(25,1), key="-FILE-"),
            sg.FileBrowse(file_types=file_types),
            sg.Button("Carregar Imagem")
        ],
        [sg.Button("Salvar")]
    ]

    window_recorte = sg.Window("Visualizador de Imagem", layout=layout_recortar)
    dragging = False
    ponto_inicial = ponto_final = retangulo = None

    while True:
        event, values = window_recorte.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        if event == "Carregar Imagem":
            filename = values["-FILE-"]
            if os.path.exists(filename):
                image = Image.open(filename)
                image.thumbnail((500,500))
                bio = io.BytesIO()
                image.save(bio, format="PNG")
                window_recorte["-IMAGE-"].draw_image(data=bio.getvalue(), location=(0,400))

        if event == "-IMAGE-":
            x, y = values["-IMAGE-"]
            if not dragging:
                ponto_inicial = (x, y)
                dragging = True
            else:
                ponto_final = (x, y)
            if retangulo:
                window_recorte["-IMAGE-"].delete_figure(retangulo)
            if None not in (ponto_inicial, ponto_final):
                retangulo = window_recorte["-IMAGE-"].draw_rectangle(ponto_inicial, ponto_final, line_color='red')


        elif event.endswith('+UP'):
            dragging = False

        if event == "Salvar":
            image = Image.open(image_path)
            cropped_image = image.crop((ponto_inicial,ponto_final))
            cropped_image.save(output_image_path)
            window_recorte.close()


def rotate(image_path, degrees_to_rotate, output_image_path):
    image_obj = Image.open(image_path)
    rotated_image = image_obj.rotate(degrees_to_rotate)
    new_image = rotated_image
    new_image.save(output_image_path)

def resize(input_image_path, output_image_path):
    image = Image.open(input_image_path)
    size_layout = [[ sg.Text("WIDTH"),
                     sg.Input(size=(25,1), key="-WIDTH-"), 
                     sg.Button("TAMANHO LARGURA")],
                    [sg.Text("HEIGHT"),
                     sg.Input(size=(25,1), key="-HEIGHT-"),
                     sg.Button("TAMANHO ALTURA"),]] 

    size_window = sg.Window("IMAGE RESIZE", size_layout)

    while True:
        events, values = size_window.read()

        if events == "Exit" or events == sg.WINDOW_CLOSED:
            break

        if events == "TAMANHO LARGURA":
            valor_width = int(values["-WIDTH-"])
            proportion =  valor_width/ image.width
            valor_height = int(image.height * proportion)

        if events == "TAMANHO ALTURA":
            valor_height = int(values["-HEIGHT-"])
            proportion =  valor_height/ image.height
            valor_width = int(image.width * proportion)

        
        print("PROPORCAO", proportion)
        resized_image = image.resize((valor_width,valor_height))
        new_image = resized_image
        new_image.save(output_image_path)
        size_window.close()


def brilho(filename, fator, output_filename):
    image = Image.open(filename)
    image.thumbnail((500,500))
    enhancer = ImageEnhance.Brightness(image)
    new_image = enhancer.enhance(fator)
    new_image.save(output_filename)

def contraste(filename, fator, output_filename):
    image = Image.open(filename)
    image.thumbnail((500,500))
    enhancer = ImageEnhance.Contrast(image)
    new_image = enhancer.enhance(fator)
    new_image.save(output_filename)

def cores(filename, fator, output_filename):
    image = Image.open(filename)   
    image.thumbnail((500,500))
    enhancer = ImageEnhance.Color(image)
    new_image = enhancer.enhance(fator)
    new_image.save(output_filename)

def nitidez(filename, fator, output_filename):
    image = Image.open(filename)
    image.thumbnail((500,500))
    enhancer = ImageEnhance.Sharpness(image)
    new_image = enhancer.enhance(fator)
    new_image.save(output_filename)

def aplica_efeito(values, tmp_file, window):
    efeito_selecionado = values["-EFEITOS-"]
    filename = values["-FILE-"]
    factor = values["-FATOR-"]
    
    if filename:
        if efeito_selecionado == "Normal":
            efeitos[efeito_selecionado](filename, tmp_file)
        else:
            efeitos[efeito_selecionado](filename, factor, tmp_file)

    
    atualizar_imagem(tmp_file, window)            
        

file_types = [("All files (*.*)", "*.*")]

tmp_file = tempfile.NamedTemporaryFile(suffix=".png").name    

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

          
efeitos = {
    "Normal": shutil.copy,
    "Brilho": brilho,
    "Cores": cores,
    "Contraste": contraste,
    "Nitidez": nitidez
}

def main():
    effect_names = list(efeitos.keys())

    menu_def = [['FILTROS', ['Thumbnail', 'Qualidade baixa', 'Preto e branco', 'Sepia', 'Diminuir cores']],
                ['EDITAR', ["ESPELHADO", "CROP", "TAMANHO"]],
                ['ROTACIONAR', ["DIREITA", "ESQUERDA"]],
                ['INFOS',["EXIF"]]]
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
        ],
        [
            sg.Text("Efeitos"),
            sg.Combo(effect_names, default_value="Normal", key="-EFEITOS-", enable_events=True, readonly=True),
            sg.Slider(range=(0, 5), default_value=2, resolution=0.1, orientation="h", enable_events=True, key="-FATOR-"),
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
            #atualizar_imagem(tmp_file, window)

        if event == "Thumbnail":
            salvar_thumbnail(filename, tmp_file) 
            atualizar_imagem(tmp_file, window)

        if event == "Qualidade baixa":
            salvar_qualidade_reduzida(filename, tmp_file)
            atualizar_imagem(tmp_file, window)

        if event == "Salvar":
            salvar(filename, formato, new_filename)

        if event == "Preto e branco":
            salvar_branco_preto(filename, tmp_file)
            atualizar_imagem(tmp_file, window)    

        if event == "Sepia":
            converte_sepia(filename, tmp_file)
            atualizar_imagem(tmp_file, window)

        if event == "Diminuir cores":
            diminuir_cor(filename, tmp_file)
            atualizar_imagem(tmp_file, window)

        if event == "EXIF":
            exif()
            atualizar_imagem(tmp_file, window)
            
        if event == "ESPELHADO":
            mirror(filename, tmp_file)
            atualizar_imagem(tmp_file, window)

        if event == "CROP":
            crop_image(filename, tmp_file)
            atualizar_imagem(tmp_file, window)
            
        if event == "DIREITA":
            rotate(filename,90, tmp_file)
            atualizar_imagem(tmp_file, window)

        if event == "ESQUERDA":
            rotate(filename,-90, tmp_file)   
            atualizar_imagem(tmp_file, window)

        if event == "TAMANHO":
            resize(filename,tmp_file)
            atualizar_imagem(tmp_file, window)

        if event in ["Carregar a Imagem", "-EFEITOS-", "-FATOR-"]:
            aplica_efeito(value, tmp_file, window)


    window.close()


if __name__ == "__main__":
    main()