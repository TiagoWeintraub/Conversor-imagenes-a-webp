import os
from PIL import Image

def convert_images_to_webp(path):
    if not os.path.exists(path):
        print(f"La ruta {path} no existe.")
        return

    # Lista de extensiones de archivo de imágenes que deseas convertir
    image_extensions = ('.png', '.jpg', '.jpeg', '.bmp', '.tiff')

    for root, dirs, files in os.walk(path):
        for file in files:
            if file.lower().endswith(image_extensions):
                file_path = os.path.join(root, file)
                output_path = os.path.splitext(file_path)[0] + '.webp'

                try:
                    with Image.open(file_path) as img:
                        img.save(output_path, 'webp')
                        print(f"Imagen convertida: {file_path} -> {output_path}")
                except Exception as e:
                    print(f"Error al convertir {file_path}: {e}")

if __name__ == "__main__":
    path = "/Users/tiago/Documents/GitHub/HelicopTourSite/assets/imagenes"  # Reemplaza esto con la ruta a tu carpeta
    convert_images_to_webp(path)
