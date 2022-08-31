from sys import platlibdir
from PIL import Image

def muda_paraa_cinza(imagem_entrada, imagem_saida):
    imagem = Image.open(imagem_entrada)
    imagem = imagem.convert("P", palette=Image.Palette.ADAPTIVE, colors = 16)
    imagem.save(imagem_saida)

if __name__ == "__main__":
    muda_paraa_cinza("Aula04/pizza.jpg", "Aula04/pizza_4cores.png")
    