from pickletools import optimize
from PIL import Image

def image_converter(input_file, output_file, formato):
    imagem = Image.open(input_file)
    imagem.save(output_file, format = formato, optimize= True, quality = 75)
    imagem.thumbnail([75,75])
    imagem.save("thumbnail_ranni.jpg")

def image_format(input_file):
    imagem = Image.open(input_file)
    print(f"Formato: {imagem.format_description}")

if __name__ == "__main__":
    image_converter("blaid&ranni.jpg", "blaid&ranni.png", "PNG")
    image_format("blaid&ranni.jpg")
    image_format("blaid&ranni.png")   
    #image_format("pizza.sptv")   
