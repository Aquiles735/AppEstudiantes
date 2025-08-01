import tkinter as tk
from tkinter import ttk

class VentanaNotas:
    def __init__(self, master):
        self.registrar_notas = tk.Toplevel(master)
        self.registrar_notas.title("Registrar Notas")

        # --- Contenedor para los campos de entrada y los botones ---
        contenedor_widgets = ttk.Frame(self.registrar_notas)
        contenedor_widgets.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # --- Widgets dentro del contenedor ---

        # Cédula de Identidad
        tk.Label(contenedor_widgets, text='Cédula:').grid(row=0, column=0, pady=5, padx=5, sticky="e")
        self.cedula_entry = tk.Entry(contenedor_widgets)
        self.cedula_entry.grid(row=0, column=1, pady=5, padx=5, sticky="w")
        self.cedula_entry.focus()

        # Nombre
        tk.Label(contenedor_widgets, text='Nombre:').grid(row=1, column=0, pady=5, padx=5, sticky="e")
        self.nombre_alumno_entry = tk.Entry(contenedor_widgets)
        self.nombre_alumno_entry.grid(row=1, column=1, pady=5, padx=5, sticky="w")
        #Apellido
        tk.Label(contenedor_widgets, text='Apellido:').grid(row=2, column=0, pady=5, padx=5, sticky="e")
        self.nombre_alumno_entry = tk.Entry(contenedor_widgets)
        self.nombre_alumno_entry.grid(row=2, column=1, pady=5, padx=5, sticky="w")

        # Nota específica
        tk.Label(contenedor_widgets, text='Evaluacion:').grid(row=3, column=0, pady=5, padx=5, sticky="e")
        opciones = ['Evaluacion 1','Evaluacion 2','Evaluacion 3','Evaluacion 4','Evaluacion 5','Evaluacion 6','Evaluacion 7']
        combobox_opciones = ttk.Combobox( contenedor_widgets,values=opciones)
        combobox_opciones.set(opciones[0]) 
        combobox_opciones.grid(row=3, column=1, padx=5, pady=5, sticky="ew")
        #valor nota
        tk.Label(contenedor_widgets, text='Nota:').grid(row=4, column=0, pady=5, padx=5, sticky="e")
        self.nombre_alumno_entry = tk.Entry(contenedor_widgets)
        self.nombre_alumno_entry.grid(row=4, column=1, pady=5, padx=5, sticky="w")

        # --- Botones en la misma fila del contenedor ---
        btn_registrar = ttk.Button(contenedor_widgets, text='Guardar Nota')
        btn_registrar.grid(row=5, column=0, pady=10, sticky="we")

        # Botón para salir
        btn_salir = ttk.Button(contenedor_widgets, text='Salir', command=self.registrar_notas.destroy)
        btn_salir.grid(row=5, column=1, pady=10, padx=(5,0), sticky="we")

        # --- Treeview debajo del contenedor ---
        self.tree = ttk.Treeview(self.registrar_notas, columns=('col0', 'col1', 'col2','col3','col4','col5','col6','col7','col8','col9','col10'), show='headings')
        self.tree.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        self.tree.heading('col0', text='Cédula', anchor='center')
        
        self.tree.heading('col1', text='Nombre', anchor='center')
        self.tree.heading('col2', text='Apellido', anchor='center')
        self.tree.heading('col3', text='Evaluacion 1', anchor='center')
        self.tree.heading('col4', text='Evaluacion 2', anchor='center')
        self.tree.heading('col5', text='Evaluacion 3', anchor='center')
        self.tree.heading('col6', text='Evaluacion 4', anchor='center')
        self.tree.heading('col7', text='Evaluacion 5', anchor='center')
        self.tree.heading('col8', text='Evaluacion 6', anchor='center')
        self.tree.heading('col9', text='Evaluacion 7', anchor='center')
        self.tree.heading('col10', text='TOTAL', anchor='center')
        self.tree.column('col0', width=150)
        self.tree.column('col1', width=200)
        self.tree.column('col2', width=200)
        self.tree.column('col3', width=100)
        self.tree.column('col4', width=100)
        self.tree.column('col5', width=100)
        self.tree.column('col6', width=100)
        self.tree.column('col7', width=100)
        self.tree.column('col8', width=100)
        self.tree.column('col9', width=100)
        self.tree.column('col10', width=100)
        