from PIL import Image
from PIL import ImageEnhance

def enhance_brightness(image_path, enhance_factor, output_path):
    image = Image.open(image_path)
    enhancer = ImageEnhance.Brightness(image)
    new_image = enhancer.enhance(enhance_factor)
    new_image.save(output_path)

if __name__ == "__main__":
    enhance_brightness("hawaii.png", 1.5,"hawaii_brigthness.png")