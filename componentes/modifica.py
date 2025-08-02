import tkinter as tk
from tkinter import ttk
import sqlite3
from tkinter import messagebox

class VentanaModificar:
    db_name = 'registro_estudiante.db'

    def __init__(self, master, estudiante_seleccionado, main_app_instance):
        self.wind = tk.Toplevel(master)
        self.wind.title("Modificar Estudiante")
        self.wind.transient(master)  # Hace que esta ventana sea modal
        self.main_app_instance = main_app_instance
        self.estudiante_data = estudiante_seleccionado

        if not self.estudiante_data:
            messagebox.showwarning("Error", "Debe seleccionar un estudiante para modificar.")
            self.wind.destroy()
            return
        
        frame = ttk.Frame(self.wind)
        frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.messaje = tk.Label(frame, text='', fg='red')
        self.messaje.grid(row=6, column=0, columnspan=2, sticky='ew')

        tk.Label(frame, text='Cédula:').grid(row=0, column=0, sticky="e", pady=5)
        self.cedula_entry = tk.Entry(frame, state='readonly')
        self.cedula_entry.grid(row=0, column=1, sticky="ew", padx=5)

        tk.Label(frame, text='Nombre:').grid(row=1, column=0, sticky="e", pady=5)
        self.nombre_entry = tk.Entry(frame)
        self.nombre_entry.grid(row=1, column=1, sticky="ew", padx=5)

        tk.Label(frame, text='Apellido:').grid(row=2, column=0, sticky="e", pady=5)
        self.apellido_entry = tk.Entry(frame)
        self.apellido_entry.grid(row=2, column=1, sticky="ew", padx=5)
        
        tk.Label(frame, text='Nivel:').grid(row=3, column=0, sticky="e", pady=5)
        opciones_nivel = ['1 año', '2 año', '3 año', '4 año', '5 año']
        self.nivel_combobox = ttk.Combobox(frame, values=opciones_nivel, state='readonly')
        self.nivel_combobox.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

        tk.Label(frame, text='Sección:').grid(row=4, column=0, sticky="e", pady=5)
        opciones_seccion = ['A','B','C','D','E','F','G']
        self.seccion_combobox = ttk.Combobox(frame, values=opciones_seccion, state='readonly')
        self.seccion_combobox.grid(row=4, column=1, padx=5, pady=5, sticky="ew")

        tk.Label(frame, text='Email:').grid(row=5, column=0, sticky="e", pady=5)
        self.email_entry = tk.Entry(frame)
        self.email_entry.grid(row=5, column=1, sticky="ew", padx=5)

        btn_modificar = ttk.Button(frame, text='Guardar Cambios', command=self.modificar_estudiante)
        btn_modificar.grid(row=7, column=0, pady=10, sticky="ew")

        btn_salir = ttk.Button(frame, text='Salir', command=self.wind.destroy)
        btn_salir.grid(row=7, column=1, pady=10, sticky="ew")

        self.load_data_to_entries()


    def run_query(self, query, parameters = ()):
        with sqlite3.connect(self.db_name) as conn:
            cursor=conn.cursor()
            result=cursor.execute(query, parameters)
            conn.commit()
        return result
    
    def load_data_to_entries(self):
        self.clear_entries()
        
        if self.estudiante_data:
            self.cedula_entry.config(state='normal')
            self.cedula_entry.insert(0, self.estudiante_data['cedula'])
            self.cedula_entry.config(state='readonly')
            self.nombre_entry.insert(0, self.estudiante_data['nombre'])
            self.apellido_entry.insert(0, self.estudiante_data['apellido'])
            self.nivel_combobox.set(self.estudiante_data['nivel'])
            self.seccion_combobox.set(self.estudiante_data['seccion'])
            self.email_entry.insert(0, self.estudiante_data['email'])

    def clear_entries(self):
        self.cedula_entry.config(state='normal')
        self.cedula_entry.delete(0, tk.END)
        self.cedula_entry.config(state='readonly')
        self.nombre_entry.delete(0, tk.END)
        self.apellido_entry.delete(0, tk.END)
        self.nivel_combobox.set('')
        self.seccion_combobox.set('')
        self.email_entry.delete(0, tk.END)
    
    def modificar_estudiante(self):
        cedula_original = self.estudiante_data['cedula']
        
        nombre_nuevo = self.nombre_entry.get()
        apellido_nuevo = self.apellido_entry.get()
        nivel_nuevo = self.nivel_combobox.get()
        seccion_nueva = self.seccion_combobox.get()
        email_nuevo = self.email_entry.get()

        if nombre_nuevo and apellido_nuevo and nivel_nuevo and seccion_nueva and email_nuevo:
            query = 'UPDATE estudiantes SET nombre = ?, apellido = ?, nivel = ?, seccion = ?, email = ? WHERE cedula_estudiante = ?'
            parameters = (nombre_nuevo, apellido_nuevo, nivel_nuevo, seccion_nueva, email_nuevo, cedula_original)
            
            self.run_query(query, parameters)
            self.messaje['text'] = f'Datos de {nombre_nuevo} actualizados.'
            
            # Llama al método get_estudiantes() de la instancia de la ventana principal
            self.main_app_instance.get_estudiantes()
            self.wind.destroy()
        else:
            self.messaje['text'] = 'Todos los campos son obligatorios.'