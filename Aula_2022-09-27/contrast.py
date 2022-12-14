from PIL import Image
from PIL import ImageEnhance

def enhance_contrast(image_path, enhance_factor, output_path):
    image = Image.open(image_path)
    enhancer = ImageEnhance.Contrast(image)
    new_image = enhancer.enhance(enhance_factor)
    new_image.save(output_path)

if __name__ == "__main__":
    enhance_contrast("hawaii.png", 2.5, "hawaii_contrast.png")