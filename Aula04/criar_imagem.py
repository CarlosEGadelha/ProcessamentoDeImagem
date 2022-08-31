from PIL import Image
from PIL import ImageColor

def cria_imagem(filename, size):
    image = Image.new("RGBA", size)

    cor1 = ImageColor.getcolor("red", "RGBA")
    cor2 = ImageColor.getcolor("yellow", "RGBA")
    cor = cor1
    count = 0

    for y in range(size[1]):
        for x in range(size[0]):
            if count == 3:
                cor = cor2 if cor1 == cor else cor1
                count = 0

            image.putpixel((x,y), cor)
            count+=1

    image.save(filename)

if __name__ == "__main__":
    cria_imagem("Aula04/imagem.png", (100,100))