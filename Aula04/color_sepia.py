from PIL import Image

def calcula_paleta(branco):
    paleta = []
    r,g,b = branco
    for i in range(255):
        new_red = r * i // 255
        new_geen = g * i // 255
        new_blue = b * i // 255
        paleta.extend((new_red, new_blue, new_geen))
    return paleta    

def converte_sepia(input, output):
    #branco = (255, 240,192)
    branco = (112, 87, 20)

    paleta = calcula_paleta(branco)

    imagem = Image.open(input)
    imagem = imagem.convert("L")
    imagem.putpalette(paleta)
    sepia = imagem.convert("RGB")

    sepia.save(output)


if __name__ == "__main__":
    converte_sepia("Aula04/pizza.jpg", "Aula04/pizza_sepia.png")