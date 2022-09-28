from PIL import Image
from PIL import ImageEnhance

def enhance_color(image_path, enhance_factor, output_path):
    image = Image.open(image_path)
    enhancer = ImageEnhance.Color(image)
    new_image = enhancer.enhance(enhance_factor)
    new_image.save(output_path)

if __name__ == "__main__":
    enhance_color("hawaii.png", 0.0, "hawaii_color.png")