import os
import base64
import json
import requests
import pandas as pd
import threading
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
from urllib.parse import quote
from google.oauth2.service_account import Credentials
import datetime
from zoneinfo import ZoneInfo

# --- 1. CONFIGURACIÓN CENTRAL ---

# Se requiere un archivo de credenciales de Google Service Account
SERVICE_ACCOUNT_FILE = "google_credentials_dummy.json" 
SPREADSHEET_NAME = "DB_Documentos_IOFE"
SHEET_NAME = "Logs"
AMBIENTE = "https://api.iofesign.com" 
CARPETA_DESTINO = "DESCARGADOS"

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

# Flujos de trabajo (IDs genéricos para demostración)
WORKFLOWS_DISPONIBLES = {
    "CLIENTE A - GLP": 1001,
    "CLIENTE A - GNV": 1002,
    "CLIENTE B - GLP": 1003,
    "CLIENTE B - GNV": 1004, 
    "CERTIFICADO CONFORMIDAD GLP": 2001,
    "CERTIFICADO CONFORMIDAD GNV": 2002,
}

# --- 2. LÓGICA DE BACKEND ---

# --- Lógica de IOFE ---

def iofe_login(username, password):
    """Intenta loguearse en IOFE y devuelve el token."""
    url = f"{AMBIENTE}/login"
    data = {"username": username, "password": password}
    try:
        resp = requests.post(url, json=data)
        if resp.status_code == 200:
            token = resp.headers.get("Authorization", "").strip()
            if token:
                return token, "Login exitoso."
            else:
                return None, "Error: Token no recibido en los headers."
        else:
            return None, f"Error de login ({resp.status_code}): {resp.text}"
    except requests.exceptions.RequestException as e:
        return None, f"Error de conexión: {e}"

def subir_documento_iofe(token, workflow_id, pdf_path, nombre_pdf):
    """Sube un solo documento a IOFE y devuelve la data de respuesta."""
    url = f"{AMBIENTE}/api/v1/outside/documents"
    headers = {
        "Authorization": token,
        "Content-Type": "application/json"
    }
    
    try:
        with open(pdf_path, "rb") as f:
            base64_pdf = base64.b64encode(f.read()).decode("utf-8")
    except Exception as e:
        return None, f"Error leyendo PDF '{nombre_pdf}': {e}"

    subject = os.path.splitext(nombre_pdf)[0]
    payload = {
        "type": 1,
        "subject": subject,
        "workflowId": workflow_id,
        "participants": [],
        "files": [{"name": nombre_pdf, "base64": base64_pdf}]
    }

    try:
        resp = requests.post(url, headers=headers, json=payload)
        if resp.status_code == 200:
            data = resp.json()
            data['subject'] = subject 
            return data, f"Documento '{nombre_pdf}' cargado a IOFE."
        else:
            return None, f"Error al subir '{nombre_pdf}' ({resp.status_code}): {resp.text}"
    except requests.exceptions.RequestException as e:
        return None, f"Error de conexión subiendo '{nombre_pdf}': {e}"

def cancelar_documento_iofe(token, document_id, motivo):
    """Cancela un solo documento en IOFE."""
    try:
        motivo_encoded = quote(motivo)
        url = f"{AMBIENTE}/api/v1/outside/documents/{document_id}/cancel?comment={motivo_encoded}"
        headers = {"Authorization": token}
        resp = requests.put(url, headers=headers)

        if resp.status_code == 200:
            return True, f"Documento {document_id} anulado en IOFE ({motivo})."
        else:
            return False, f"Error al anular {document_id} ({resp.status_code}): {resp.text}"
    except requests.exceptions.RequestException as e:
        return False, f"Error de conexión anulando {document_id}: {e}"

# --- NUEVAS FUNCIONES DE DESCARGA ---
def obtener_link_descarga(token, document_id):
    """Consulta los detalles del documento para obtener el link de descarga."""
    url = f"{AMBIENTE}/api/v1/outside/documents/{document_id}"
    headers = {"Authorization": token}
    try:
        resp = requests.get(url, headers=headers)
        if resp.status_code == 200:
            data = resp.json()
            stream_link = data.get("_links", {}).get("stream", {}).get("href")
            if stream_link:
                return stream_link, "Link de descarga obtenido."
            return None, "❌ Error: No se encontró 'stream_link' en la respuesta."
        return None, f"❌ Error API ({resp.status_code}): {resp.text}"
    except requests.exceptions.RequestException as e:
        return None, f"❌ Error de conexión: {e}"

def descargar_pdf(url, nombre_archivo, carpeta_destino):
    """Descarga un PDF desde una URL y lo guarda localmente."""
    try:
        r = requests.get(url) 
        if r.status_code == 200:
            os.makedirs(carpeta_destino, exist_ok=True)
            ruta = os.path.join(carpeta_destino, f"{nombre_archivo}-signed.pdf")
            with open(ruta, "wb") as f:
                f.write(r.content)
            return True, f"📥 Descargado: {ruta}"
        else:
            return False, f"❌ Error al descargar {nombre_archivo} ({r.status_code})"
    except Exception as e:
        return False, f"❌ Error al guardar archivo: {e}"

# --- Lógica de Google Sheets (Requiere credenciales reales para funcionar) ---

def get_gsheet_client():
    """Conecta con Google Sheets y devuelve el cliente."""
    if not os.path.exists(SERVICE_ACCOUNT_FILE):
        raise FileNotFoundError(f"No se encontró el archivo de credenciales: {SERVICE_ACCOUNT_FILE}")
        
    creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    client = None
    try:
        import gspread
        client = gspread.authorize(creds)
    except ImportError:
        raise ImportError("La librería gspread no está instalada.")
        
    sheet = client.open(SPREADSHEET_NAME).worksheet(SHEET_NAME)
    return sheet

def append_record_gsheet(sheet, io_data, workflow_id):
    """Añade una fila al Google Sheet."""
    fecha = datetime.datetime.now(tz=ZoneInfo("America/Lima")).isoformat()
    row = [
        io_data.get('subject', 'N/A'),
        str(io_data.get("id", 'N/A')),
        fecha,
        io_data.get("hashIdentifier", ""),
        io_data.get("_links", {}).get("stream", {}).get("href", ""),
        str(workflow_id),
        "Activo" # Status inicial
    ]
    try:
        sheet.append_row(row, value_input_option="USER_ENTERED")
        return True, "Registro añadido a Google Sheets."
    except Exception as e:
        return False, f"Error al escribir en Google Sheets: {e}"

def batch_lookup_gsheet(sheet, subjects):
    """Busca masivamente IDs de documentos por subject."""
    try:
        all_values = sheet.get_all_values()
        if not all_values or len(all_values) < 2:
            return {}, "Hoja vacía o sin cabeceras."

        headers = [h.strip() for h in all_values[0]]
        # Creamos un índice de headers para búsqueda robusta
        header_index = {h: i for i, h in enumerate(headers)}
        
        # Validamos que las columnas necesarias existan
        if "Subject" not in header_index or "IOFE_ID" not in header_index:
            return None, "Error: La hoja debe tener columnas 'Subject' y 'IOFE_ID'."

        idx_subject = header_index["Subject"]
        idx_id = header_index["IOFE_ID"]
        idx_workflow = header_index.get("workFlowID") 

        index = {}
        for row in all_values[1:]:
            try:
                subject_val = row[idx_subject].strip()
                if subject_val in subjects:
                    index[subject_val] = {
                        "IOFE_ID": row[idx_id].strip(),
                        "workflowId": row[idx_workflow].strip() if idx_workflow and len(row) > idx_workflow else None
                    }
            except IndexError:
                continue 
        
        results = {}
        for s in subjects:
            results[s] = index.get(s) 
            
        return results, "Búsqueda en Sheets completada."
    except Exception as e:
        return None, f"Error en batch_lookup: {e}"

def update_status_gsheet(sheet, subject, new_status="Anulado"):
    """Actualiza el estado de un 'subject' en Google Sheets."""
    try:
        cell = sheet.find(subject, in_column=1) 
        if not cell:
            return False, f"No se encontró el subject '{subject}' en la hoja."
        
        # Asumimos que Status es la columna 7 (G)
        sheet.update_cell(cell.row, 7, new_status)
        return True, f"Estado de '{subject}' actualizado a '{new_status}' en Sheets."
    except Exception as e:
        return False, f"Error al actualizar estado de '{subject}': {e}"

# --- 3. APLICACIÓN GUI (Tkinter) ---

class App(tk.Tk):
    """Clase principal de la aplicación."""
    def __init__(self):
        super().__init__()
        self.title("Gestor de Firmas IOFE - Portfolio Edition")
        self.geometry("700x600")

        # Variables de estado compartidas
        self.iofe_token = None
        self.iofe_username = tk.StringVar()
        self.iofe_password = tk.StringVar()
        self.gsheet_client = None

        # Contenedor principal
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        # Crear las 4 pantallas (Frames)
        for F in (LoginFrame, CargaFrame, AnulacionFrame, DescargaFrame):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("LoginFrame")

    def show_frame(self, page_name):
        """Muestra un frame por su nombre."""
        frame = self.frames[page_name]
        frame.tkraise()
    
    def attempt_gsheet_connect(self):
        """Intenta conectar con Google Sheets y almacena el cliente."""
        try:
            self.gsheet_client = get_gsheet_client()
            return True
        except FileNotFoundError:
            # En modo portfolio, permitimos continuar sin credenciales reales para ver la UI
            messagebox.showwarning("Modo Demo", "No se encontró archivo de credenciales. Algunas funciones estarán limitadas.")
            return False
        except Exception as e:
            messagebox.showerror("Error de Google", f"No se pudo conectar a Google Sheets:\n{e}")
            return False

class LoginFrame(tk.Frame):
    """Pantalla de Login."""
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Estilo
        s = ttk.Style()
        s.configure('TButton', font=('Helvetica', 12))
        s.configure('Header.TLabel', font=('Helvetica', 20, 'bold'))

        # Layout
        frame_login = ttk.Frame(self, padding="20 40")
        frame_login.place(relx=0.5, rely=0.3, anchor="center")

        ttk.Label(frame_login, text="LOGIN", style='Header.TLabel').pack(pady=20)
        
        ttk.Label(frame_login, text="Usuario").pack(pady=(10,0))
        entry_user = ttk.Entry(frame_login, textvariable=self.controller.iofe_username, width=40)
        entry_user.pack()

        ttk.Label(frame_login, text="Contraseña").pack(pady=(10,0))
        entry_pass = ttk.Entry(frame_login, textvariable=self.controller.iofe_password, show="*", width=40)
        entry_pass.pack()

        btn_login = ttk.Button(frame_login, text="INICIAR SESIÓN", command=self.perform_login, style='TButton')
        btn_login.pack(pady=20, ipadx=10, ipady=5)
        
        # Contenedor de botones de acción
        frame_actions = ttk.Frame(self, padding="20 20")
        frame_actions.place(relx=0.5, rely=0.7, anchor="center")
        frame_actions.columnconfigure(0, weight=1)
        frame_actions.columnconfigure(1, weight=1)

        self.btn_cargar = ttk.Button(frame_actions, text="CARGAR DOCUMENTOS", 
                                     command=lambda: controller.show_frame("CargaFrame"), state="disabled")
        self.btn_anular = ttk.Button(frame_actions, text="ANULAR FIRMAS", 
                                     command=lambda: controller.show_frame("AnulacionFrame"), state="disabled")
        self.btn_descargar = ttk.Button(frame_actions, text="DESCARGAR DOCUMENTOS",
                                        command=lambda: controller.show_frame("DescargaFrame"), state="disabled")

        self.btn_cargar.grid(row=0, column=0, padx=10, pady=5, ipadx=20, ipady=10, sticky="ew")
        self.btn_anular.grid(row=0, column=1, padx=10, pady=5, ipadx=20, ipady=10, sticky="ew")
        self.btn_descargar.grid(row=1, column=0, columnspan=2, padx=10, pady=(10,0), ipadx=20, ipady=10, sticky="ew")


    def perform_login(self):
        """Maneja el evento de click en 'INICIAR SESIÓN'."""
        user = self.controller.iofe_username.get()
        pwd = self.controller.iofe_password.get()
        
        # En modo demo, simulamos login si se usa usuario 'demo'
        if user == "demo":
            self.controller.iofe_token = "dummy_token_12345"
            messagebox.showinfo("Login Exitoso", "Sesión iniciada en Modo Demo.")
            self.btn_cargar.config(state="normal")
            self.btn_anular.config(state="normal")
            self.btn_descargar.config(state="normal")
            return

        if not user or not pwd:
            messagebox.showwarning("Login", "Usuario y contraseña no pueden estar vacíos.")
            return

        # 1. Conectar a Google Sheets primero
        if not self.controller.gsheet_client:
            self.controller.attempt_gsheet_connect()

        # 2. Conectar a IOFE
        token, msg = iofe_login(user, pwd)
        if token:
            self.controller.iofe_token = token
            messagebox.showinfo("Login Exitoso", msg)
            self.btn_cargar.config(state="normal")
            self.btn_anular.config(state="normal")
            self.btn_descargar.config(state="normal")
        else:
            messagebox.showerror("Error de Login", msg)
            self.controller.iofe_token = None
            self.btn_cargar.config(state="disabled")
            self.btn_anular.config(state="disabled")
            self.btn_descargar.config(state="disabled")


class CargaFrame(tk.Frame):
    """Pantalla de Carga de Documentos."""
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.carpeta_seleccionada = tk.StringVar()
        self.flujo_seleccionado = tk.StringVar()

        btn_volver = ttk.Button(self, text="⬅ Volver", command=lambda: controller.show_frame("LoginFrame"))
        btn_volver.pack(anchor="nw", padx=10, pady=10)

        frame_main = ttk.Frame(self, padding="10 20")
        frame_main.pack(fill="x", expand=True)

        ttk.Label(frame_main, text="CARGA DE DOCUMENTOS", style='Header.TLabel').pack(pady=10)

        # 1. Selección de Carpeta
        frame_folder = ttk.Frame(frame_main)
        frame_folder.pack(fill="x", pady=10)
        ttk.Label(frame_folder, text="Seleccionar carpeta:").pack(anchor="w")
        
        frame_path = ttk.Frame(frame_folder)
        frame_path.pack(fill="x", expand=True)
        entry_path = ttk.Entry(frame_path, textvariable=self.carpeta_seleccionada, state="readonly", width=70)
        entry_path.pack(side="left", fill="x", expand=True, padx=(0, 10))
        btn_buscar = ttk.Button(frame_path, text="Buscar", command=self.seleccionar_carpeta)
        btn_buscar.pack(side="left")

        # 2. Selección de Flujo
        ttk.Label(frame_main, text="Seleccione flujo:").pack(anchor="w", pady=(20, 0))
        self.combo_flujo = ttk.Combobox(frame_main, textvariable=self.flujo_seleccionado, 
                                        values=list(WORKFLOWS_DISPONIBLES.keys()), state="readonly")
        self.combo_flujo.pack(fill="x")
        if WORKFLOWS_DISPONIBLES:
            self.combo_flujo.current(0) 

        # 3. Botón de Carga
        self.btn_cargar = ttk.Button(frame_main, text="CARGAR", style='TButton', command=self.iniciar_carga)
        self.btn_cargar.pack(pady=20, ipadx=20, ipady=10)

        # 4. Log de Salida
        ttk.Label(frame_main, text="Log de carga:").pack(anchor="w")
        self.log_area = scrolledtext.ScrolledText(frame_main, height=15, wrap=tk.WORD, state="disabled")
        self.log_area.pack(fill="both", expand=True)
        
    def seleccionar_carpeta(self):
        path = filedialog.askdirectory()
        if path:
            self.carpeta_seleccionada.set(path)

    def log(self, message):
        self.log_area.config(state="normal")
        self.log_area.insert(tk.END, f"{message}\n")
        self.log_area.see(tk.END) 
        self.log_area.config(state="disabled")

    def iniciar_carga(self):
        folder = self.carpeta_seleccionada.get()
        flujo_nombre = self.flujo_seleccionado.get()
        
        if not folder:
            messagebox.showwarning("Validación", "Por favor, seleccione una carpeta.")
            return
        if not flujo_nombre:
            messagebox.showwarning("Validación", "Por favor, seleccione un flujo de trabajo.")
            return
        
        self.log_area.config(state="normal")
        self.log_area.delete(1.0, tk.END) 
        self.log_area.config(state="disabled")
        self.btn_cargar.config(state="disabled") 

        token = self.controller.iofe_token
        workflow_id = WORKFLOWS_DISPONIBLES[flujo_nombre]
        sheet = self.controller.gsheet_client
        
        thread = threading.Thread(target=self.proceso_de_carga_thread, 
                                  args=(token, workflow_id, folder, sheet), daemon=True)
        thread.start()

    def proceso_de_carga_thread(self, token, workflow_id, folder, sheet):
        self.log("🚀 Iniciando proceso de carga masiva...")
        self.log(f"Flujo seleccionado: {self.flujo_seleccionado.get()} (ID: {workflow_id})")
        
        try:
            pdfs = [f for f in os.listdir(folder) if f.lower().endswith(".pdf")]
            if not pdfs:
                self.log("⚠️ No se encontraron archivos PDF en la carpeta especificada.")
                self.btn_cargar.config(state="normal")
                return

            self.log(f"Se encontraron {len(pdfs)} archivos PDF.")
            exitos = 0
            errores = 0
            
            for i, pdf in enumerate(pdfs, 1):
                self.log(f"\n--- ({i}/{len(pdfs)}) Procesando: '{pdf}' ---")
                ruta_pdf = os.path.join(folder, pdf)
                
                # Simulación si no hay API real accesible
                if token == "dummy_token_12345":
                    self.log("Modo Demo: Simulación de carga exitosa.")
                    exitos += 1
                    continue

                # 1. Subir a IOFE
                data_iofe, msg_iofe = subir_documento_iofe(token, workflow_id, ruta_pdf, pdf)
                self.log(f"IOFE: {msg_iofe}")

                if data_iofe and sheet:
                    # 2. Registrar en Google Sheets
                    ok_gsheet, msg_gsheet = append_record_gsheet(sheet, data_iofe, workflow_id)
                    self.log(f"GSheets: {msg_gsheet}")
                    if ok_gsheet:
                        exitos += 1
                    else:
                        errores += 1
                elif data_iofe and not sheet:
                     self.log("GSheets: Omitido (sin conexión)")
                     exitos += 1
                else:
                    errores += 1
            
            self.log("\n--- ✅ PROCESO FINALIZADO ---")
            self.log(f"Éxitos: {exitos} | Errores: {errores}")

        except Exception as e:
            self.log(f"\n❌ ERROR INESPERADO: {e}")
        
        self.btn_cargar.config(state="normal")

# (Las clases AnulacionFrame y DescargaFrame seguirían la misma lógica de sanitización)
# Para mantener la brevedad en el portafolio, se asume su implementación similar.

class AnulacionFrame(tk.Frame):
    # Implementación similar sanitizada
    def __init__(self, parent, controller):
        super().__init__(parent)
        ttk.Label(self, text="PANTALLA DE ANULACIÓN (Código Sanitizado)").pack(pady=20)
        ttk.Button(self, text="⬅ Volver", command=lambda: controller.show_frame("LoginFrame")).pack()

class DescargaFrame(tk.Frame):
    # Implementación similar sanitizada
    def __init__(self, parent, controller):
        super().__init__(parent)
        ttk.Label(self, text="PANTALLA DE DESCARGA (Código Sanitizado)").pack(pady=20)
        ttk.Button(self, text="⬅ Volver", command=lambda: controller.show_frame("LoginFrame")).pack()

# --- 4. PUNTO DE ENTRADA ---
if __name__ == "__main__":
    app = App()
    app.mainloop()