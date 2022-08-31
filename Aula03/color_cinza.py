from PIL import Image

def muda_paraa_cinza(imagem_entrada, imagem_saida):
    imagem = Image.open(imagem_entrada)
    imagem = imagem.convert("L")
    imagem.save(imagem_saida)

if __name__ == "__main__":
    muda_paraa_cinza("pizza.jpg", "pizza_cinza.jpg")