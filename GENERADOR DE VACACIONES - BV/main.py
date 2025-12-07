import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pandas as pd
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
import os
import sys
from datetime import date
import re
import threading
from pathlib import Path

# --- CONFIGURACIÓN GENÉRICA ---
# Nombre de la carpeta donde se guardarán los resultados
OUTPUT_DIR_BASE = 'Salida_Certificados'
# Nombre del archivo plantilla (debe estar en la misma carpeta al compilar)
TEMPLATE_FILE = 'template.html'
# Nombre del logo genérico
IMAGE_FILE = 'logo.jpg'

def resource_path(relative_path):
    """
    Obtiene la ruta absoluta del recurso.
    Funciona tanto en entorno de desarrollo (Python) como en el .exe compilado (PyInstaller).
    """
    try:
        # PyInstaller crea una carpeta temporal y guarda la ruta en _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def generar_pdfs_logic(excel_path, progress_bar, status_label):
    """
    Lógica principal de generación de PDFs.
    Ejecutada en un hilo secundario para no congelar la interfaz.
    """
    try:
        # 1. Crear estructura de carpetas de salida
        dir_a = os.path.join(OUTPUT_DIR_BASE, 'Division_A')
        dir_b = os.path.join(OUTPUT_DIR_BASE, 'Division_B')
        os.makedirs(dir_a, exist_ok=True)
        os.makedirs(dir_b, exist_ok=True)

        # 2. Configurar Jinja2
        template_path = resource_path(TEMPLATE_FILE)
        # Verificamos que exista el template antes de continuar
        if not os.path.exists(template_path):
            raise FileNotFoundError(f"No se encontró la plantilla: {TEMPLATE_FILE}")
            
        env = Environment(loader=FileSystemLoader(os.path.dirname(template_path)))
        template = env.get_template(os.path.basename(template_path))

        # 3. Leer el archivo de Excel
        status_label.config(text="Leyendo base de datos...")
        df = pd.read_excel(excel_path)
        total_records = len(df)
        progress_bar['maximum'] = total_records

        # 4. Contexto de fecha actual (Día de la generación/firma)
        hoy = date.today()
        meses_es = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", 
                    "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
        
        contexto_fecha = {
            'DIA_FIRMA': hoy.day,
            'MES_FIRMA': meses_es[hoy.month - 1],
            'ANIO_FIRMA': hoy.year,
            'PERIODO_ACTUAL': hoy.year
        }

        # 5. Iterar sobre cada empleado
        for index, row in df.iterrows():
            nombre = row.get('APELLIDOS_NOMBRES', f'Registro {index+1}')
            status_label.config(text=f"Procesando: {nombre}...")
            
            # Convertir fila de pandas a diccionario para Jinja2
            context = row.to_dict()
            context.update(contexto_fecha)

            # Formatear fechas del Excel (asumiendo formato datetime)
            for campo_fecha in ['FECHA_INICIO', 'FECHA_TERMINO', 'FECHA_RETORNO']:
                if campo_fecha in row and pd.notnull(row[campo_fecha]):
                     context[campo_fecha] = pd.to_datetime(row[campo_fecha]).strftime('%d/%m/%Y')
                else:
                     context[campo_fecha] = "N/A"

            # Lógica de División/Empresa (Generalizada)
            # En el Excel la columna debe decir 'DIV_A' o 'DIV_B' (o lo adaptas)
            division = str(row.get('DIVISION', '')).strip().upper()
            
            if division == 'DIV_A':
                output_folder = dir_a
                context['MARCA_A'], context['MARCA_B'] = 'X', '' # Para marcar casillas en el HTML
            elif division == 'DIV_B':
                output_folder = dir_b
                context['MARCA_A'], context['MARCA_B'] = '', 'X'
            else:
                output_folder = os.path.join(OUTPUT_DIR_BASE, 'Otros')
                os.makedirs(output_folder, exist_ok=True)
                context['MARCA_A'], context['MARCA_B'] = '', ''

            # Renderizar HTML con los datos
            html_renderizado = template.render(context)

            # Nombre del archivo seguro (sin caracteres especiales)
            pdf_filename = re.sub(r'[\\/*?:"<>|]', "", f"Doc - {nombre}.pdf")
            output_path = os.path.join(output_folder, pdf_filename)
            
            # Generar PDF
            # Base_url es necesario para que WeasyPrint encuentre las imágenes locales
            base_dir = Path(resource_path('.')).as_uri() + "/"
            HTML(string=html_renderizado, base_url=base_dir).write_pdf(output_path)
            
            # Actualizar progreso
            progress_bar['value'] = index + 1
            progress_bar.update()

        messagebox.showinfo("Éxito", f"Se generaron {total_records} documentos correctamente.")
        status_label.config(text="Proceso finalizado.")

    except FileNotFoundError as e:
        messagebox.showerror("Archivo Faltante", f"Error: {e}")
    except KeyError as e:
        messagebox.showerror("Error de Datos", f"Columna faltante en Excel: {e}")
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error inesperado:\n{e}")
    finally:
        generate_button.config(state=tk.NORMAL)
        progress_bar['value'] = 0
        status_label.config(text="")

def start_generation():
    excel_path = entry_path.get()
    if not excel_path or not os.path.exists(excel_path):
        messagebox.showwarning("Atención", "Seleccione un archivo Excel válido.")
        return
    
    generate_button.config(state=tk.DISABLED)
    progress_bar['value'] = 0
    
    # Threading para evitar congelamiento de GUI
    thread = threading.Thread(target=generar_pdfs_logic, args=(excel_path, progress_bar, status_label))
    thread.start()

def select_file():
    filepath = filedialog.askopenfilename(
        title="Seleccionar Base de Datos",
        filetypes=[("Archivos de Excel", "*.xlsx *.xls")]
    )
    if filepath:
        entry_path.delete(0, tk.END)
        entry_path.insert(0, filepath)

# --- GUI ---
root = tk.Tk()
root.title("Automatización de Documentos - Demo")
root.geometry("500x250")
root.resizable(False, False)

frame = tk.Frame(root, padx=15, pady=15)
frame.pack(expand=True, fill=tk.BOTH)

top_frame = tk.Frame(frame)
top_frame.pack(fill=tk.X)

label_file = tk.Label(top_frame, text="Input (Excel):")
label_file.pack(side=tk.LEFT, padx=(0, 10))

entry_path = tk.Entry(top_frame)
entry_path.pack(side=tk.LEFT, expand=True, fill=tk.X)

button_select = tk.Button(top_frame, text="Buscar", command=select_file)
button_select.pack(side=tk.LEFT, padx=(10, 0))

generate_button = tk.Button(frame, text="Iniciar Automatización", font=("Arial", 11, "bold"), 
                            command=start_generation, bg="#2196F3", fg="white", height=2)
generate_button.pack(pady=20, fill=tk.X)

status_label = tk.Label(frame, text="Esperando archivo...", fg="grey")
status_label.pack(fill=tk.X)
progress_bar = ttk.Progressbar(frame, orient='horizontal', mode='determinate')
progress_bar.pack(fill=tk.X, pady=5)

root.mainloop()