
from tkinter import filedialog
import tkinter as tk
import customtkinter as ctk
from customtkinter import filedialog
from datetime import datetime
import pandas as pd
import dbfread
import glob
from pandastable import Table, TableModel # Importar clases de pandastable




def seleccionar_archivo():
    root = tk.Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    file_path = filedialog.askopenfile()
    return file_path

#FUNCION TRANSFORMAR FECHAS


def transformar_fecha2(fecha):
    patrones = ["%d-%m-%Y", "%d%m%Y", "%Y-%m-%d", "%d-%B-%Y","%d/%m/%Y %H:%M:%S","%Y-%m-%d %H:%M:%S" ]
    for patron in patrones:
        try:
            fecha_transformada = datetime.strptime(fecha, patron).strftime("%d-%m-%Y")
            return fecha_transformada
        except ValueError:
            pass
    return None
  
#def transformar_fecha(df, columna):
 #   df[columna]=pd.to_datetime(df[columna], dayfirst=True, errors='coerce')
  #  df[columna] = df[columna].fillna('01-01-1900')
   # df[columna] = df[columna].dt.strftime("%d-%m-%Y")
    #return df
    
    
    
def subir_dbf():
    archivo = None
    root = tk.Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    print(archivo)
    while True:
        archivo = filedialog.askopenfile()
        if archivo:
            ruta_archivo = archivo.name
            try:
                dbf =  dbfread.DBF( ruta_archivo )
                liquidacion = pd.DataFrame(dbf)
                #indicadores = pd.read_excel(ruta_archivo, engine='openpyxl')
                #padron = pd.read_csv(archivo, sep=";", encoding="ISO-8859-1")
            
                break
            except UnicodeDecodeError:
                print("Error de decodificación de caracteres. Intenta con otra codificación o archivo.")
                continue
    else:
            print("Archivo incorrecto. Por favor, vuelva a cargarlo.")
