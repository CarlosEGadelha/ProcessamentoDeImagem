from pickletools import optimize
from PIL import Image

def image_converter(input_file, output_file, formato):
    imagem = Image.open(input_file)
    imagem.save(output_file, format = formato, optimize= True, quality = 75)
    imagem.thumbnail([75,75])
    imagem.save("thumbnail.jpg")

def image_format(input_file):
    imagem = Image.open(input_file)
    print(f"Formato: {imagem.format_description}")

if __name__ == "__main__":
    image_converter("pizza.jpg", "pizza_jpg2.png", "jpeg")
    image_format("pizza.jpg")
    image_format("pizza.png")   
    image_format("pizza.sptv")   
