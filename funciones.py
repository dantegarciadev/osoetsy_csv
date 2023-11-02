
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
    patrones = ["%d-%m-%Y", "%Y-%m-%d","%d/%m/%Y", "%d-%m-%Y","%d/%m/%Y %H:%M:%S","%Y-%m-%d %H:%M:%S"]
    for patron in patrones:
        try:
            fecha_transformada = datetime.strptime(fecha, patron).strftime("%d/%m/%Y")
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
    file_path = None # Inicializar la variable file_path
    liquidacion = None # Inicializar la variable liquidacion
    continuar = True # Crear una variable booleana para controlar el bucle
    while continuar: # Usar la variable continuar como condición del bucle
        root = tk.Tk()
        root.withdraw()
        root.attributes('-topmost', True)
        file_path = filedialog.askopenfilename() # Usar el método askopenfilename para obtener la ruta del archivo
        print(file_path) # Imprimir la ruta del archivo
        if file_path and file_path.endswith('.DBF'): # Comprobar si se ha seleccionado un archivo dbf válido
            try:
                dbf =  dbfread.DBF(file_path) # Leer el archivo dbf con dbfread
                liquidacion = pd.DataFrame(dbf) # Crear el dataframe con pandas
                print(liquidacion) # Imprimir el dataframe
                continuar = False # Cambiar la variable continuar a False para salir del bucle
            except (UnicodeDecodeError, FileNotFoundError, PermissionError, ValueError) as e: # Capturar varias excepciones posibles al leer el archivo dbf
                print(f"Error al leer el archivo dbf: {e}. Intenta con otro archivo o codificación.")
                continuar = True # Mantener la variable continuar en True para repetir el bucle
        else: # Si no se ha seleccionado un archivo dbf válido
            print("Archivo incorrecto. Por favor, vuelve a cargarlo o cancela la operación.")
            continuar = True # Mantener la variable continuar en True para repetir el bucle
    return liquidacion # Devolver el dataframe creado con pandas al final de la función