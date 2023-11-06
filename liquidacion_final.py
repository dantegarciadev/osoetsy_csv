import pandas as pd
import numpy as np
import xlwt
import xlrd
from tkinter import filedialog
import tkinter as tk
import customtkinter as ctk
from customtkinter import filedialog
import openpyxl
import dbfread
import glob
from pandastable import Table, TableModel # Importar clases de pandastable
import datetime


liquidacion = None 

# Crear función para seleccionar archivos
def select_files():
    global files # Variable global para almacenar la lista de archivos
    files = filedialog.askopenfilenames(filetypes=[("Excel files", "*.xls")]) # Seleccionar solo archivos xlsx
    print(files) # Imprimir la lista de archivos

# Crear función para leer archivos y crear lista de dataframes
def read_files():
    global df_list # Variable global para almacenar la lista de dataframes
    df_list = [] # Crear lista vacía
    for file in files: # Iterar sobre cada archivo
        df = pd.read_excel(file) # Leer el archivo y saltar la primera fila
        nombre = 'FC ' + file.split("/")[-1].split(".")[0] # Extraer el nombre del archivo sin la extensión
        df["Facturas"] = nombre # Crear una nueva columna con el nombre del archivo
        df_list.append(df) # Añadir el dataframe a la lista
    print(df_list) # Imprimir la lista de dataframes

# Crear función para concatenar dataframes y crear uno nuevo
def concat_dfs():
    global df_final # Variable global para almacenar el dataframe final
    df_final = pd.concat(df_list, ignore_index=True) # Concatenar los dataframes de la lista y reiniciar el índice
    print(df_final) # Imprimir el dataframe final

#crear funcion para subir dbf
def subir_dbf():
    global liquidacion 
    file_path = None # Inicializar la variable file_path
    #liquidacion = None # Inicializar la variable liquidacion
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
                continuar = False # Cambiar la variable continuar a False para salir del bucle
            except (UnicodeDecodeError, FileNotFoundError, PermissionError, ValueError) as e: # Capturar varias excepciones posibles al leer el archivo dbf
                print(f"Error al leer el archivo dbf: {e}. Intenta con otro archivo o codificación.")
                continuar = True # Mantener la variable continuar en True para repetir el bucle
        else: # Si no se ha seleccionado un archivo dbf válido
            print("Archivo incorrecto. Por favor, vuelve a cargarlo o cancela la operación.")
            continuar = True # Mantener la variable continuar en True para repetir el bucle
    return liquidacion # Devolver el dataframe creado con pandas al final de la función

# Crear función para hacer merge left entre df_final y liquidacion
def merge_dfs():
    global merge_filtrado # Variable global para almacenar el dataframe resultante del merge
    df_merge = pd.merge(df_final, liquidacion, how='left', left_on='ben_id', right_on='BEN_ID') # Hacer el merge left por la columna BEN_ID
    merge_filtrado = df_merge[['Facturas','OS_NOMBRE','os_nombre','ori_nom','ord_fec', 'it_cod','importe','nombreafi','nom_nom' ]]
    print(df_merge) # Imprimir el dataframe resultante

# Crear función para separar el dataframe resultante por la columna convenio
def split_dfs():
    global dfs # Variable global para almacenar la lista de dataframes separados
    groups = merge_filtrado.groupby('OS_NOMBRE') # Agrupar el dataframe por la columna convenio
    dfs = [] # Crear una lista vacía para almacenar los dataframes separados
    for name, group in groups: # Iterar sobre los grupos y añadir cada dataframe a la lista
        dfs.append(group)
    print(dfs) # Imprimir la lista de dataframes

# Crear función para mostrar dataframe con pandastable
def show_df():
    global table # Variable global para almacenar el objeto Table
    table = Table(frame, dataframe=df_final, visiblecols=True) # Crear objeto Table dentro del Frame
    table.show() # Mostrar la tabla en la ventana

# Crear función para seleccionar una carpeta donde guardar los dataframes
def select_folder():
    global folder # Variable global para almacenar la ruta de la carpeta
    folder = filedialog.askdirectory() # Mostrar el diálogo para seleccionar la carpeta
    print(folder) # Imprimir la ruta de la carpeta

# Crear funcion para unir los diferentes archiovos de excel
def seleccionar_excels():
    global excel_lista_archivos # la definimos como global para guardar para usarla en la funcion "save_excel_final"
    # creamos una lista vacia para guardar las direcciones de los archivos de excel
    excel_lista_archivos=[]
    # usamos el bucle while para que la ventana siga abriendose hasta que se cancele la seleccion
    while True:
        # usamos el widget filedialog.askopenfilename() para obtener el nombre y la direccion de excel
        excel_archivos = filedialog.askopenfilename(title="Selecciona un archivo de Excel", filetypes=("archivos excel",".xlsx"))
        # Si se cancela la seleccion el bucle se rompe
        if excel_archivos == "":
            break
        # Mientras siga, se va agregando la lista de direcciones de archivos a las lista  excel_lista_archivos=[]
        else:
            excel_lista_archivos.append(excel_archivos)

# Crear una funcion para unir los archvos guardados en en la lista "taxcel_lista_archivos"
def juntar_archivos_exel(excel_lista_archivos):
    # usa la variable global df_unido
    global df_unido
    # creo un dataframe vacio y le asigno la variable df_unido
    df_unido = pd.DataFrame()
    # recorremos la lista "excel_lista_archivos" de Excel
    for excel_archivos in excel_lista_archivos:
        # leemos la lista excel_lista_archivos y agregamos al dataframe con append()
        df1 = pd.read_excel(excel_archivos)
        df_unido = df_unido.append(df1)
        print(df_unido)
        # mostramos mensaje indicando que se completo el proceso
    tk.messagebox.showinfo(title="Proceso Completado", message="Se creo el archivo con todos los Excels seleccionados")


# Funcion para guardar el dataframe en un archivo excel
def guardar_excel_final():
    # usar la variable global df_unido
    global df_unido
    global nombre_final
    #tomar la hora 
    ahora = datetime.datetime.now()
    # Formatear la fecha y hora como una cadena con el formato "aaaa-mm-dd hh:mm:ss"
    fecha = ahora.strftime("%Y-%m-%d %H-%M-%S")

    # revisa si el dataframe esta vacio
    if df_unido is None or df_unido.empty:
        # si esta vacio va a mostrar el mensaje "no hay datos para guardar"
        tk.messagebox.showerror(title="Error", message="No hay datos para guardar. Selecciona primero los archivos de Excel que quieres unir.")
    else:
        # si esta vacio usa el widget filedialog.asksaveasfilename() para obtener la ruta y el nombre del archivo a guardar
        excel_final = filedialog.askdirectory(title="guardar excel final")
        nombre = df_unido.iloc[2, df_unido.columns.get_loc("OS_NOMBRE")]
        nombre_final = excel_final + "/" + nombre + "_final " + fecha + ".xlsx"
        if excel_final == "":
            # si se cancelo no hace nada
            pass
        else:
            # si no se cancelo, uso un try-excep para manejar los errores
            try:
                df_unido.to_excel(nombre_final, index = False)
                tk.messagebox.showinfo(title="Archivo guardado", message=f"Se ha guardado el archivo '{nombre}'")
            except Exception as e:
                # si ocurre un error, muestra el mensaje con el tipo de error
                tk.messagebox.showerror(title="Error", message=f"ha ocurrido un error al guardar el archivo: {e}")
    




# Crear función para guardar cada dataframe en un archivo excel con el nombre del convenio
def save_dfs():
    for df in dfs: # Iterar sobre la lista de dataframes
        convenio = df['OS_NOMBRE'].iloc[0] # Obtener el nombre del convenio del primer elemento del grupo
        filename = folder + '/' + convenio + '.xlsx' # Crear el nombre del archivo con la ruta de la carpeta y el nombre del convenio
        df.to_excel(filename, index=False) # Guardar el dataframe en el archivo excel sin el índice
        print(f"Se ha guardado el archivo {filename}") # Imprimir un mensaje de confirmación

###########################################################################################################
################################## BOTONES   #############################################################
#########################################################################################################

# Crear interfaz gráfica
window = tk.Tk() # Crear ventana principal
window.title("Procesar Liquidaciones") # Asignar título a la ventana
window.geometry("800x600") # Ancho 800, alto calculado


# Crear un widget Frame dentro de la ventana
frame = tk.Frame(window)
frame.pack()

# Crear botón para seleccionar archivos
btn_select = tk.Button(window, text="Seleccionar liquidaciones", command=lambda: [select_files(), read_files(), concat_dfs()])
btn_select.pack() # Colocar el botón en la ventana

# Crear botón para mostrar dataframe con pandastable
btn_show = tk.Button(window, text="Mostrar liquidacion armada(opcinal)", command=show_df)
btn_show.pack() # Colocar el botón en la ventana

# Crear botón para seleccionar padrón DBF
btn_select = tk.Button(window, text="Seleccionar padrón", command= lambda:subir_dbf())
btn_select.pack() # Colocar el botón en la ventana

#btn_process = tk.Button(window, text="Procesar archivos", command=lambda:[merge_dfs(), split_dfs(), tk.messagebox.showinfo
#("Proceso completado", "Los archivos se han procesado correctamente")])
#btn_process.pack()

# Crear botón para llamar a las funciones anteriores y mostrar un mensaje
btn_save = tk.Button(window, text="procesar y Guardar convenios", command=lambda:[merge_dfs(), split_dfs(),select_folder(), save_dfs(), tk.messagebox.showinfo("Archivos Procesados y guardados correctamente","Archivos Procesados y guardados correctamente" )])
btn_save.pack()


#Crear boton para unir los archivos creados de convenios desde varios directorios .
btn_save = tk.Button(window, text="Unir Archivos", command=lambda:[seleccionar_excels(), tk.messagebox.showinfo(title="ARchivos unidos correctamente", message="Archivos Unidos" )])
btn_save.pack()


btn_save = tk.Button(window, text="Guardar Archivos", command=lambda:[juntar_archivos_exel(excel_lista_archivos),guardar_excel_final(), tk.messagebox.showinfo(title="excel_guardado", message= "El archivo se guardo en la Carpeta seleccionada")])
btn_save.pack()
# Guardar el archivo final_
window.mainloop() # Iniciar el bucle principal de la ventana
