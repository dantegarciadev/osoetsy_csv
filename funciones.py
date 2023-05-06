
from tkinter import filedialog
import tkinter as tk
import customtkinter as ctk
from customtkinter import filedialog


def seleccionar_archivo():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfile()
    return file_path

