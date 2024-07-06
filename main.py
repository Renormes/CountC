import tkinter as tk
from tkinter import messagebox
import openpyxl
import os
import shutil
from ultralytics import YOLO
from PIL import Image
import cv2
import pandas as pd
from concurrent.futures import ThreadPoolExecutor

if not os.path.exists("contagens"):
    os.makedirs("contagens")

def setup_directories(dirs):
    for dir_info in dirs:
        if os.path.exists(dir_info["path"]):
            shutil.rmtree(dir_info["path"])
            # time.sleep(1)  # Removed sleep
        os.makedirs(dir_info["path"])
        for sub_dir in dir_info.get("sub_dirs", []):
            os.makedirs(os.path.join(dir_info["path"], sub_dir))
        # time.sleep(1)  # Removed sleep

directories = [
    {"path": "cutQuadrantes"},
    {"path": "cortes", "sub_dirs": ["q1", "q2", "q3", "q4"]},
    {"path": "countCell", "sub_dirs": ["q1", "q2", "q3", "q4"]}
]

setup_directories(directories)

diretorios = [
    'predict', 'predict2', 'predict3', 'predict4', 'predict5',
    'predict6', 'predict7', 'predict8', 'predict9', 'predict10',
    'predict11', 'predict12', 'predict13', 'predict14', 'predict15', 'predict16'
]

cells = [
    ('C9', 'C10'), ('E9', 'E10'), ('G9', 'G10'), ('I9', 'I10'),
    ('C11', 'C12'), ('E11', 'E12'), ('G11', 'G12'), ('I11', 'I12'),
    ('C13', 'C14'), ('E13', 'E14'), ('G13', 'G14'), ('I13', 'I14'),
    ('C15', 'C16'), ('E15', 'E16'), ('G15', 'G16'), ('I15', 'I16'),
    ('L9', 'L10'), ('N9', 'N10'), ('P9', 'P10'), ('R9', 'R10'),
    ('L11', 'L12'), ('N11', 'N12'), ('P11', 'P12'), ('R11', 'R12'),
    ('L13', 'L14'), ('N13', 'N14'), ('P13', 'P14'), ('R13', 'R14'),
    ('L15', 'L16'), ('N15', 'N16'), ('P15', 'P16'), ('R15', 'R16'),
    ('C19', 'C20'), ('E19', 'E20'), ('G19', 'G20'), ('I19', 'I20'),
    ('C21', 'C22'), ('E21', 'E22'), ('G21', 'G22'), ('I21', 'I22'),
    ('C23', 'C24'), ('E23', 'E24'), ('G23', 'G24'), ('I23', 'I24'),
    ('C25', 'C26'), ('E25', 'E26'), ('G25', 'G26'), ('I25', 'I26'),
    ('L19', 'L20'), ('N19', 'N20'), ('P19', 'P20'), ('R19', 'R20'),
    ('L21', 'L22'), ('N21', 'N22'), ('P21', 'P22'), ('R21', 'R22'),
    ('L23', 'L24'), ('N23', 'N24'), ('P23', 'P24'), ('R23', 'R24'),
    ('L25', 'L26'), ('N25', 'N26'), ('P25', 'P26'), ('R25', 'R26')
]

cellers = []

def submit():
    try:
        nome = f'contagens/celulas_{entry0.get()}.xlsx'

        if os.path.exists(nome):
            messagebox.showinfo("showinfo", "Codigo de amostra ja utilizado")
            return

        shutil.copyfile('contagem.xlsx', nome)

        workbook = openpyxl.load_workbook(nome)
        worksheet = workbook.active
        worksheet['S4'].value = int(entry1.get())
        worksheet['S5'].value = int(entry2.get())
        worksheet['S6'].value = int(entry3.get())
        workbook.save(nome)

        model = YOLO('trainsquares.pt')

        with ThreadPoolExecutor() as executor:
            for filenamer in os.listdir("quadrantes/"):
                img_pil = Image.open(f"quadrantes/{filenamer}")

                executor.submit(process_image, model, img_pil)

        count_cells()
        update_excel(nome)

        os.startfile(os.path.realpath(nome))

    except ValueError:
        messagebox.showerror("Error", "Erro inesperado")

def process_image(model, img_pil):
    results_img_pil = model.predict(
        source=img_pil,
        conf=0.25,
        iou=0.7,
        imgsz=640,
        show=False,
        save=False,
        save_txt=False,
        save_conf=True,
        save_crop=True,
        project='cutQuadrantes',
        stream=False
    )
    process_images()

def process_images():
    for dirname in os.listdir("cutQuadrantes/"):
        crop_path = f"cutQuadrantes/{dirname}/crops/"
        for dire in os.listdir(crop_path):
            dire_path = os.path.join(crop_path, dire)
            for filename in os.listdir(dire_path):
                image_p = os.path.join(dire_path, filename)
                process_single_image(image_p, dire, filename)

def process_single_image(image_p, dire, filename):
    output_f = image_p
    image = cv2.imread(image_p)
    if image is None:
        print(f"Error: Could not open image at {image_p}")
        exit(1)
    negative_image = 255 - image
    cv2.imwrite(output_f, negative_image)
    split_count_image(image_p, f"cortes/{dire}", dire, filename)

def split_count_image(image_path, output_folder, dire, filename):
    input_image = Image.open(image_path)
    width, height = input_image.size
    sub_width = width // 4
    sub_height = height // 4

    model = YOLO('traincell.pt')

    for row in range(4):
        for col in range(4):
            left = col * sub_width
            upper = row * sub_height
            right = left + sub_width
            lower = upper + sub_height

            sub_image = input_image.crop((left, upper, right, lower))
            sub_image_filename = f"{dire}_{row}_{col}_{filename}"
            sub_image_path = os.path.join(output_folder, sub_image_filename)
            sub_image.save(sub_image_path)

            model.predict(
                source=sub_image_path,
                conf=0.25,
                iou=0.7,
                imgsz=640,
                show=False,
                save=False,
                save_txt=True,
                save_conf=False,
                save_crop=False,
                project=f'countCell/{dire}',
                stream=False
            )

def count_cells():
    for direse in os.listdir("countCell/"):
        for diretorio in diretorios:
            path_labels = os.path.join("countCell", direse, diretorio, 'labels')
            if not os.path.exists(path_labels):
                continue

            arquivos_txt = [file for file in os.listdir(path_labels) if file.endswith('.txt')]
            if arquivos_txt:
                for filenames in arquivos_txt:
                    with open(os.path.join(path_labels, filenames), 'r') as file:
                        lines = file.readlines()
                        classe_0 = sum(1 for line in lines if line.startswith('0'))
                        classe_1 = sum(1 for line in lines if line.startswith('1'))
                    cellers.append([classe_0, classe_1])
            else:
                cellers.append([0, 0])

def update_excel(nome):
    file_paths = nome
    spreadsheet = pd.ExcelFile(file_paths)
    sheet_name = 'cell counter'
    df = spreadsheet.parse(sheet_name)

    workbook = openpyxl.load_workbook(file_paths)
    worksheet = workbook[sheet_name]

    for cell_pair, vector in zip(cells, cellers):
        worksheet[cell_pair[0]] = vector[0]
        worksheet[cell_pair[1]] = vector[1]

    workbook.save(file_paths)

def submit_images():
    try:
        if os.path.exists('quadrantes'):
            shutil.rmtree('quadrantes')
        os.makedirs('quadrantes')
        os.startfile("quadrantes")

    except ValueError:
        messagebox.showerror("Error", "Algum erro inesperado aconteceu")

root = tk.Tk()
root.title("Contador de Celulas")

tk.Label(root, text="Codigo das celulas usadas=").grid(row=0, column=0, padx=10, pady=5)
entry0 = tk.Entry(root)
entry0.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="Vol. total da suspensão de celulas=").grid(row=1, column=0, padx=10, pady=5)
entry1 = tk.Entry(root)
entry1.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="Vol. de celulas retirado da suspensao (antes de adicionar tripan)=").grid(row=2, column=0, padx=10, pady=5)
entry2 = tk.Entry(root)
entry2.grid(row=2, column=1, padx=10, pady=5)

tk.Label(root, text="Vol. de tripan adicionado as celulas=").grid(row=3, column=0, padx=10, pady=5)
entry3 = tk.Entry(root)
entry3.grid(row=3, column=1, padx=10, pady=5)

submit_button = tk.Button(root, text="Subir 4 imagens", command=submit_images)
submit_button.grid(row=4, column=0, columnspan=2, pady=10)

submit_button = tk.Button(root, text="Contar celulas nas imagens", command=submit)
submit_button.grid(row=5, column=0, columnspan=2, pady=10)

root.mainloop()