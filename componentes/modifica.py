import tkinter as tk
from tkinter import ttk
import sqlite3
from tkinter import messagebox

class VentanaModificar:
    db_name = 'registro_estudiante.db'

    def __init__(self, master, cedula_estudiante_orig, nombre_orig, apellido_orig, nivel_orig, seccion_orig, callback_actualizar):
        self.wind = tk.Toplevel(master)
        self.wind.title("Modificar Estudiante")
        self.wind.transient(master) 
        self.wind.grab_set() 
        self.wind.resizable(False, False)
        self.wind.config(bg='#34495e')
        
        self.cedula_original = cedula_estudiante_orig
        self.callback_actualizar = callback_actualizar

        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TFrame', background='#34495e')
        style.configure('TLabel', background='#34495e', foreground='#ecf0f1', font=('Helvetica', 10))
        style.configure('TEntry', fieldbackground='#ecf0f1', foreground='#2c3e50', font=('Helvetica', 10))
        style.configure('TCombobox', fieldbackground='#ecf0f1', foreground='#2c3e50', font=('Helvetica', 10))
        style.configure('TButton', background='#3498db', foreground='white', font=('Helvetica', 10, 'bold'), borderwidth=1)
        style.map('TButton', background=[('active', '#2980b9')])

        frame = ttk.Frame(self.wind)
        frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        self.messaje = tk.Label(frame, text='', bg='#34495e', fg='#e74c3c', font=('Helvetica', 10, 'bold'))
        self.messaje.grid(row=5, column=0, columnspan=2, sticky='ew', pady=5)

        ttk.Label(frame, text='Cédula:').grid(row=0, column=0, sticky="e", pady=5)
        self.cedula_entry = ttk.Entry(frame, state='readonly')
        self.cedula_entry.grid(row=0, column=1, sticky="ew", padx=5)
        self.cedula_entry.insert(0, cedula_estudiante_orig)

        ttk.Label(frame, text='Nombre:').grid(row=1, column=0, sticky="e", pady=5)
        self.nombre_entry = ttk.Entry(frame)
        self.nombre_entry.grid(row=1, column=1, sticky="ew", padx=5)
        self.nombre_entry.insert(0, nombre_orig)

        ttk.Label(frame, text='Apellido:').grid(row=2, column=0, sticky="e", pady=5)
        self.apellido_entry = ttk.Entry(frame)
        self.apellido_entry.grid(row=2, column=1, sticky="ew", padx=5)
        self.apellido_entry.insert(0, apellido_orig)
        
        ttk.Label(frame, text='Nivel:').grid(row=3, column=0, sticky="e", pady=5)
        opciones_nivel = ['1 año', '2 año', '3 año', '4 año', '5 año','6 año']
        self.nivel_combobox = ttk.Combobox(frame, values=opciones_nivel, state='readonly')
        self.nivel_combobox.grid(row=3, column=1, padx=5, pady=5, sticky="ew")
        self.nivel_combobox.set(nivel_orig)

        ttk.Label(frame, text='Sección:').grid(row=4, column=0, sticky="e", pady=5)
        opciones_seccion = ['A','B','C','D','E','F','G','H']
        self.seccion_combobox = ttk.Combobox(frame, values=opciones_seccion, state='readonly')
        self.seccion_combobox.grid(row=4, column=1, padx=5, pady=5, sticky="ew")
        self.seccion_combobox.set(seccion_orig)
        
        btn_modificar = ttk.Button(frame, text='Guardar Cambios', command=self.modificar_estudiante)
        btn_modificar.grid(row=6, column=0, pady=10, padx=5, sticky="ew")
        btn_modificar.bind('<Return>', lambda event: btn_modificar.invoke())

        btn_salir = ttk.Button(frame, text='Salir', command=self.wind.destroy)
        btn_salir.grid(row=6, column=1, pady=10, padx=5, sticky="ew")
        btn_salir.bind('<Return>', lambda event: btn_salir.invoke())
        
        self.wind.update_idletasks()
        width = self.wind.winfo_width()
        height = self.wind.winfo_height()
        x = (self.wind.winfo_screenwidth() // 2) - (width // 2)
        y = (self.wind.winfo_screenheight() // 2) - (height // 2)
        self.wind.geometry(f'{width}x{height}+{x}+{y}')

    def run_query(self, query, parameters = ()):
        with sqlite3.connect(self.db_name) as conn:
            cursor=conn.cursor()
            result=cursor.execute(query, parameters)
            conn.commit()
        return result
    
    def modificar_estudiante(self):
        nombre_nuevo = self.nombre_entry.get()
        apellido_nuevo = self.apellido_entry.get()
        nivel_nuevo = self.nivel_combobox.get()
        seccion_nueva = self.seccion_combobox.get()

        if nombre_nuevo and apellido_nuevo and nivel_nuevo and seccion_nueva:
            if not nombre_nuevo.istitle() or not apellido_nuevo.istitle():
                self.messaje.config(fg='#e74c3c')
                self.messaje['text'] = 'El Nombre y Apellido deben comenzar con mayúscula.'
                return

            query = 'UPDATE estudiantes SET nombre = ?, apellido = ?, nivel = ?, seccion = ? WHERE cedula_estudiante = ?'
            parameters = (nombre_nuevo, apellido_nuevo, nivel_nuevo, seccion_nueva, self.cedula_original)
            
            try:
                self.run_query(query, parameters)
                self.messaje.config(fg='#2ecc71')
                self.messaje['text'] = f'Datos de {nombre_nuevo} actualizados.'
                
                self.callback_actualizar()
                messagebox.showinfo("Éxito", f"Datos de {nombre_nuevo} actualizados correctamente.")
                self.wind.destroy()
            except Exception as e:
                self.messaje.config(fg='#e74c3c')
                self.messaje['text'] = f'Error al actualizar: {e}'
        else:
            self.messaje.config(fg='#e74c3c')
            self.messaje['text'] = 'Todos los campos son obligatorios.'