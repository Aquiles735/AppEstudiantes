import tkinter as tk
from tkinter import ttk
import sqlite3
from tkinter import messagebox
from modifica.widgets_modifica import create_widgets # Importa la nueva función


class VentanaModificar:
    db_name = 'registro_estudiante.db'


    def __init__(self, master, cedula_estudiante_orig, nombre_orig, apellido_orig, nivel_orig, seccion_orig, callback_actualizar):
        # Llama a la función que crea los widgets
        create_widgets(self, master, cedula_estudiante_orig, nombre_orig, apellido_orig, nivel_orig, seccion_orig)
        
        # Estas líneas se mantienen en __init__ porque son específicas de la clase
        self.cedula_original = cedula_estudiante_orig
        self.callback_actualizar = callback_actualizar
    
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