import tkinter as tk
from tkinter import ttk
import sqlite3

class VentanaNotas:
    db_name = 'registro_estudiante.db'
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


        # Nota específica
        tk.Label(contenedor_widgets, text='Evaluacion:').grid(row=1, column=0, pady=5, padx=5, sticky="e")
        opciones = ['Evaluacion 1','Evaluacion 2','Evaluacion 3','Evaluacion 4','Evaluacion 5','Evaluacion 6','Evaluacion 7']
        combobox_opciones = ttk.Combobox( contenedor_widgets,values=opciones)
        combobox_opciones.set(opciones[0]) 
        combobox_opciones.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        #valor nota
        tk.Label(contenedor_widgets, text='Nota:').grid(row=2, column=0, pady=5, padx=5, sticky="e")
        self.nombre_alumno_entry = tk.Entry(contenedor_widgets)
        self.nombre_alumno_entry.grid(row=2, column=1, pady=5, padx=5, sticky="w")

        # --- Botones en la misma fila del contenedor ---
        btn_registrar = ttk.Button(contenedor_widgets, text='Guardar Nota')
        btn_registrar.grid(row=3, column=0, pady=10, sticky="we")

        # Botón para salir
        btn_salir = ttk.Button(contenedor_widgets, text='Salir', command=self.registrar_notas.destroy)
        btn_salir.grid(row=3, column=1, pady=10, padx=(5,0), sticky="we")

        # --- Treeview debajo del contenedor ---
        self.tree = ttk.Treeview(self.registrar_notas, columns=('col1', 'col2','col3','col4','col5','col6','col7','col8','col9','col10'), show='headings')
        self.tree.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        
        self.tree.heading('col1', text='Cédula', anchor='center')
        self.tree.heading('col2', text='Eval 1', anchor='center')
        self.tree.heading('col3', text='Eval 2', anchor='center')
        self.tree.heading('col4', text='Eval 3', anchor='center')
        self.tree.heading('col5', text='Eval 4', anchor='center')
        self.tree.heading('col6', text='Eval 5', anchor='center')
        self.tree.heading('col7', text='Eval 6', anchor='center')
        self.tree.heading('col8', text='Eval 7', anchor='center')
        self.tree.heading('col9', text='Promedio', anchor='center')
        self.tree.heading('col10', text='TOTAL', anchor='center')
       
       
        self.tree.column('col1', width=100)
        self.tree.column('col2', width=50)
        self.tree.column('col3', width=50)
        self.tree.column('col4', width=50)
        self.tree.column('col5', width=50)
        self.tree.column('col6', width=50)
        self.tree.column('col7', width=50)
        self.tree.column('col8', width=50)
        self.tree.column('col9', width=100)
        self.tree.column('col10', width=100)

        self.get_product()  
    #   base de datos registro_estudiante.db
    def run_query(self, query, parameters = ()):
        with sqlite3.connect(self.db_name) as conn:
            cursor=conn.cursor()
            result=cursor.execute(query, parameters)
            conn.commit()
        return result
    
    def get_product(self):
         # ---  LIMPIAR EL TREEVIEW ANTES DE RECARGAR ---
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)
                   
                   #codigo SQL
        query ='SELECT * FROM notas'
        db_rows=self.run_query(query)
        for row in db_rows:
            self.tree.insert('', 'end', text=row[0], values=( row[1], row[2], row[3], row[4], row[5], row[6],row[7],row[8],row[9],row[10]))
        
        