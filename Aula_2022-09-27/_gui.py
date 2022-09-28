import io
import os
import PySimpleGUI as sg
import shutil
import tempfile

from PIL import Image
from PIL import ImageEnhance

def brilho(filename, fator, output_filename):
    image = Image.open(filename)
    enhancer = ImageEnhance.Brightness(image)
    new_image = enhancer.enhance(fator)
    new_image.save(output_filename)

def contraste(filename, fator, output_filename):
    image = Image.open(filename)
    enhancer = ImageEnhance.Contrast(image)
    new_image = enhancer.enhance(fator)
    new_image.save(output_filename)

def cores(filename, fator, output_filename):
    image = Image.open(filename)
    enhancer = ImageEnhance.Color(image)
    new_image = enhancer.enhance(fator)
    new_image.save(output_filename)

def nitidez(filename, fator, output_filename):
    image = Image.open(filename)
    enhancer = ImageEnhance.Sharpness(image)
    new_image = enhancer.enhance(fator)
    new_image.save(output_filename)

efeitos = {
    "Normal": shutil.copy,
    "Brilho": brilho,
    "Cores": cores,
    "Contraste": contraste,
    "Nitidez": nitidez
}

def aplica_efeito(values, window):
    efeito_selecionado = values["-EFEITOS-"]
    filename = values["-FILENAME-"]
    factor = values["-FATOR-"]
    
    if filename:
        if efeito_selecionado == "Normal":
            efeitos[efeito_selecionado](filename, tmp_file)
        else:
            efeitos[efeito_selecionado](filename, factor, tmp_file)
        
        image = Image.open(tmp_file)
        image.thumbnail((400, 400))
        bio = io.BytesIO()
        image.save(bio, format="PNG")
        window["-IMAGE-"].update(data=bio.getvalue(), size=(400, 400))

def save_image(filename):
    save_filename = sg.popup_get_file("Salvar", file_types=file_types, save_as=True, no_window=True)
    if save_filename == filename:
        sg.popup_error("Você não pode substituir a imagem original!")
    else:
        if save_filename:
            shutil.copy(tmp_file, save_filename)
            sg.popup(f"Arquivo {save_filename}, salvo com sucesso!")

file_types = [("JPEG (*.jpg)", "*.jpg"), ("PNG (*.png)", "*.png"), ("All files (*.*)", "*.*")]
tmp_file = tempfile.NamedTemporaryFile(suffix=".jpg").name

def main():
    effect_names = list(efeitos.keys())
    layout = [
        [sg.Image(key="-IMAGE-", size=(400, 400))],
        [
            sg.Text("Imagem: "),
            sg.Input(size=(25, 1), key="-FILENAME-"),
            sg.FileBrowse(file_types=file_types),
            sg.Button("Carregar a Imagem")
        ],
        [
            sg.Text("Efeito"),
            sg.Combo(effect_names, default_value="Normal", key="-EFEITOS-", enable_events=True, readonly=True),
            sg.Slider(range=(0, 5), default_value=2, resolution=0.1, orientation="h", enable_events=True, key="-FATOR-"),
        ],
        [sg.Button("Salvar Imagem")],
    ]
    window = sg.Window("Projeto - Aula 08", layout, size=(500, 550))

    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        if event in ["Carregar a Imagem", "-EFEITOS-", "-FATOR-"]:
            aplica_efeito(values, window)
        filename = values["-FILENAME-"]
        if event == "Salvar Imagem" and filename:
            save_image(filename)
    window.close()

if __name__ == "__main__":
    main()