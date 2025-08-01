import tkinter as tk
from tkinter import ttk

class VentanaProfesor:
    def __init__(self, master):
        self.agregar_profesor = tk.Toplevel(master)
        self.agregar_profesor.title("Agregar Profesor")

        # --- Contenedor para los campos de entrada, el botón y el botón de salir ---
        contenedor_widgets = ttk.Frame(self.agregar_profesor)
        contenedor_widgets.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # --- Widgets dentro del contenedor ---
        tk.Label(contenedor_widgets, text='Nombre:').grid(row=0, column=0, pady=5, padx=5, sticky="e")
        self.nombre_entry = tk.Entry(contenedor_widgets)
        self.nombre_entry.grid(row=0, column=1, pady=5, padx=5, sticky="w")
        self.nombre_entry.focus()

        tk.Label(contenedor_widgets, text='Apellido:').grid(row=1, column=0, pady=5, padx=5, sticky="e")
        self.apellido_entry = tk.Entry(contenedor_widgets)
        self.apellido_entry.grid(row=1, column=1, pady=5, padx=5, sticky="w")

        tk.Label(contenedor_widgets, text='Email:').grid(row=2, column=0, pady=5, padx=5, sticky="e")
        self.email_entry = tk.Entry(contenedor_widgets)
        self.email_entry.grid(row=2, column=1, pady=5, padx=5, sticky="w")

        # Botones en la misma fila del contenedor
        btn_registrar = ttk.Button(contenedor_widgets, text='Registrar Profesor')
        btn_registrar.grid(row=3, column=0, pady=10, sticky="we")

        # Botón para salir
        btn_salir = ttk.Button(contenedor_widgets, text='Salir', command=self.agregar_profesor.destroy)
        btn_salir.grid(row=3, column=1, pady=10, padx=(5,0), sticky="we")

        # --- Treeview debajo del contenedor ---
        self.tree = ttk.Treeview(self.agregar_profesor, columns=('col0', 'col1', 'col2'), show='headings')
        self.tree.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        self.tree.heading('col0', text='Nombre', anchor='center')
        self.tree.heading('col1', text='Apellido', anchor='center')
        self.tree.heading('col2', text='Email', anchor='center')
        self.tree.column('col0', width=200)
        self.tree.column('col1', width=200)
        self.tree.column('col2', width=300)