
from tkinter import filedialog
import tkinter as tk
import customtkinter as ctk
from customtkinter import filedialog
from datetime import datetime




def seleccionar_archivo():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfile()
    return file_path

#FUNCION TRANSFORMAR FECHAS


def transformar_fecha(fecha):
    patrones = ["%d-%m-%Y", "%d%m%Y", "%Y-%m-%d", "%d-%B-%Y","%d/%m/%Y %H:%M:%S" ]
    for patron in patrones:
        try:
            fecha_transformada = datetime.strptime(fecha, patron).strftime("%d/%m/%Y")
            return fecha_transformada
        except ValueError:
            pass
    return None