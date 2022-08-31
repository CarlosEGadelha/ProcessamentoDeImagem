from PIL import ImageColor

def pega_valor_rgba(color):
    return ImageColor.getcolor(color, "CMYK")

if __name__ == "__main__":

    for color in ImageColor.colormap:
        print(f"{color} = {pega_valor_rgba(color)}")
