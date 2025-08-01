import tkinter as tk
from tkinter import ttk
from tkinter import *
import sqlite3
# --- Importamos la clase VentanaProfesor del archivo profesor.py ---
from componentes.profesor import VentanaProfesor

class Control:
    # nombre base de datos, para conectar la ya creada BD
    db_name = 'Institucional.db'

    def __init__(self, window):
        self.wind = window
        self.wind.title('Inicio Registro')
        
        # Contenedor para el registro de estudiantes
        frame = LabelFrame(self.wind, text='Registro Estudiante')
        frame.grid(row=0, column=0, columnspan=3, pady=20, padx=100)
        
        # --- Widgets de la ventana principal ---
        # Nivel de estudio
        Label(frame, text='Nivel:').grid(row=0, column=0)
        opciones = ['1 año', '2 año', '3 año', '4 año', '5 año']
        combobox_opciones = ttk.Combobox(frame, values=opciones)
        combobox_opciones.set(opciones[0]) 
        combobox_opciones.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        
        # Sección de estudio
        Label(frame, text='Seccion:').grid(row=0, column=2)
        opciones = ['A','B','C','D','E','F','G']
        combobox_opciones = ttk.Combobox(frame, values=opciones)
        combobox_opciones.set(opciones[0]) 
        combobox_opciones.grid(row=0, column=3, padx=5, pady=5, sticky="ew")

        # Nombre y Apellido
        Label(frame, text='Nombre:').grid(row=1, column=0)
        self.nombre=Entry(frame)
        self.nombre.grid(row=1, column=1)

        Label(frame, text='Apellido:').grid(row=1, column=2)
        self.apellido=Entry(frame)
        self.apellido.grid(row=1, column=3)      

        # Botones
        ttk.Button(frame, text='Registrar Estudiante').grid(row=2, column=1, columnspan=3, sticky=W+E)
        ttk.Button(self.wind, text='Registrar Prof.', command=self.agregar_profesor).grid(row=4, column=0, columnspan=1, sticky=W + E)
        
        # Treeview principal
        self.tree=ttk.Treeview(self.wind, columns=('col0', 'col1', 'col2', 'col3'), show='headings')
        self.tree.grid(row=5, column=0, padx=10, pady=10, sticky="nsew")
        self.tree.heading('col0', text='Nivel', anchor=CENTER)
        self.tree.heading('col1', text='Seccion', anchor=CENTER)
        self.tree.heading('col2', text='Nombre', anchor=CENTER)
        self.tree.heading('col3', text='Apellido', anchor=CENTER)
        self.tree.column('col0', width=100)
        self.tree.column('col1', width=50)
        self.tree.column('col2', width=300)
        self.tree.column('col3', width=300)
        
    def agregar_profesor(self):     
        # --- Al hacer clic en el botón, se crea una instancia de la clase VentanaProfesor ---
        VentanaProfesor(self.wind)

if __name__ == '__main__':
    window = Tk()
    apliclation = Control(window)
    window.mainloop()
# en PythonCrud iniciar aplicación 
# python3 index2.py
# para git, github abrir AppPythonCrud
