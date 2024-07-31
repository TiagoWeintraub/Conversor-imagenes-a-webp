import os
from PIL import Image
from tkinter import Tk, Label, Button, Checkbutton, IntVar, filedialog, messagebox

try:
    import pyheif
    HEIC_SUPPORTED = True
except ImportError:
    HEIC_SUPPORTED = False



import os
from PIL import Image
from subprocess import run, PIPE

def convert_heic_to_png(input_path, output_path):
    command = ['convert', input_path, output_path]
    result = run(command, stdout=PIPE, stderr=PIPE)
    if result.returncode != 0:
        print(f"Error al convertir {input_path}: {result.stderr.decode('utf-8')}")
        return False
    return True

def convert_images_to_webp(paths):
    image_extensions = ('.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.gif', '.ico', '.svg', '.heic')

    if not paths:
        print("No se seleccionaron archivos ni carpetas.")
        return

    for path in paths:
        if os.path.isfile(path):
            file_paths = [path]
        else:
            file_paths = []
            for root, dirs, files in os.walk(path):
                for file in files:
                    if file.lower().endswith(image_extensions):
                        file_paths.append(os.path.join(root, file))

        for file_path in file_paths:
            output_path = os.path.splitext(file_path)[0] + '.webp'
            try:
                if file_path.lower().endswith('.heic'):
                    intermediate_path = os.path.splitext(file_path)[0] + '.png'
                    if not convert_heic_to_png(file_path, intermediate_path):
                        continue
                    file_path = intermediate_path

                with Image.open(file_path) as img:
                    img.save(output_path, 'webp')
                    print(f"Imagen convertida: {file_path} -> {output_path}")

                if file_path.endswith('.png') and file_path.lower().endswith('.heic'):
                    os.remove(file_path)  # Elimina el archivo intermedio PNG
            except Exception as e:
                print(f"Error al convertir {file_path}: {e}")


def select_files():
    global selected_paths
    filetypes = [("Image Files", "*.png *.jpg *.jpeg *.bmp *.tiff *.gif *.ico *.svg")]
    if HEIC_SUPPORTED:
        filetypes[0] = ("Image Files", "*.png *.jpg *.jpeg *.bmp *.tiff *.gif *.ico *.svg *.heic")
    selected_paths = list(filedialog.askopenfilenames(filetypes=filetypes))
    if selected_paths:
        execute_button.config(state="normal")
    else:
        messagebox.showwarning("Advertencia", "No se seleccionaron archivos.")

def select_directory():
    global selected_paths
    path = filedialog.askdirectory()
    if path:
        selected_paths = [path]
        execute_button.config(state="normal")
    else:
        selected_paths = []
        messagebox.showwarning("Advertencia", "No se seleccionó ninguna carpeta.")

def on_select_option():
    global selected_paths
    selected_paths = []  # Limpiar la lista primero
    if var_files.get() == 1 and var_directory.get() == 0:
        select_files()
    elif var_files.get() == 0 and var_directory.get() == 1:
        select_directory()
    else:
        messagebox.showwarning("Advertencia", "Por favor, selecciona solo una opción.")

def execute_conversion():
    if selected_paths:
        convert_images_to_webp(selected_paths)
    else:
        messagebox.showwarning("Advertencia", "No se seleccionaron archivos ni carpetas.")

if __name__ == "__main__":
    global selected_paths
    selected_paths = []

    root = Tk()
    root.title("Conversor de Imágenes a WebP")
    root.geometry("400x250")

    var_files = IntVar()
    var_directory = IntVar()

    Label(root, text="Selecciona una opción:").pack(pady=10)
    Checkbutton(root, text="Archivos", variable=var_files, onvalue=1, offvalue=0).pack(pady=5)
    Checkbutton(root, text="Carpeta", variable=var_directory, onvalue=1, offvalue=0).pack(pady=5)
    Button(root, text="Seleccionar", command=on_select_option).pack(pady=10)
    execute_button = Button(root, text="Ejecutar", command=execute_conversion, state="disabled")
    execute_button.pack(pady=20)

    root.mainloop()
