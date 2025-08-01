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

        # Nombre del Alumno
        tk.Label(contenedor_widgets, text='Nombre Alumno:').grid(row=1, column=0, pady=5, padx=5, sticky="e")
        self.nombre_alumno_entry = tk.Entry(contenedor_widgets)
        self.nombre_alumno_entry.grid(row=1, column=1, pady=5, padx=5, sticky="w")

        # Nota
        tk.Label(contenedor_widgets, text='Nota:').grid(row=2, column=0, pady=5, padx=5, sticky="e")
        self.nota_entry = tk.Entry(contenedor_widgets)
        self.nota_entry.grid(row=2, column=1, pady=5, padx=5, sticky="w")

        # --- Botones en la misma fila del contenedor ---
        btn_registrar = ttk.Button(contenedor_widgets, text='Guardar Nota')
        btn_registrar.grid(row=3, column=0, pady=10, sticky="we")

        # Botón para salir
        btn_salir = ttk.Button(contenedor_widgets, text='Salir', command=self.registrar_notas.destroy)
        btn_salir.grid(row=3, column=1, pady=10, padx=(5,0), sticky="we")

        # --- Treeview debajo del contenedor ---
        self.tree = ttk.Treeview(self.registrar_notas, columns=('col0', 'col1', 'col2'), show='headings')
        self.tree.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        self.tree.heading('col0', text='Cédula', anchor='center')
        self.tree.heading('col1', text='Nombre Alumno', anchor='center')
        self.tree.heading('col2', text='Nota', anchor='center')
        self.tree.column('col0', width=150)
        self.tree.column('col1', width=300)
        self.tree.column('col2', width=100)