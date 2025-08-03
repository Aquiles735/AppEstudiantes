import tkinter as tk
from tkinter import ttk
from tkinter import *
import sqlite3
from tkinter import messagebox

# Importa las clases de las otras ventanas
from componentes.notas import VentanaNotas
from componentes.modifica import VentanaModificar

class Control:
    db_name = 'registro_estudiante.db'

    def __init__(self, window):
        self.wind = window
        self.wind.title('Inicio Registro')
        
        frame = LabelFrame(self.wind, text='Registro Estudiante')
        frame.grid(row=0, column=0, columnspan=3, pady=20, padx=100)
        
        # --- Widgets de la ventana principal ---
        Label(frame, text='Cedula').grid(row=0, column=0)
        self.cedula_entry = Entry(frame)
        self.cedula_entry.grid(row=0, column=1)

        Label(frame, text='Nombre').grid(row=0, column=2)
        self.nombre_entry = Entry(frame)
        self.nombre_entry.grid(row=0, column=3)  

        Label(frame, text='Apellido').grid(row=1, column=0)
        self.apellido_entry = Entry(frame)
        self.apellido_entry.grid(row=1, column=1)

        Label(frame, text='Nivel').grid(row=1, column=2)
        opciones_nivel = ['1 año', '2 año', '3 año', '4 año', '5 año']
        self.nivel_combobox = ttk.Combobox(frame, values=opciones_nivel)
        self.nivel_combobox.set(opciones_nivel[0]) 
        self.nivel_combobox.grid(row=1, column=3, padx=5, pady=5, sticky="ew")
        
        Label(frame, text='Seccion').grid(row=2, column=0)
        opciones_seccion = ['A','B','C','D','E','F','G']
        self.seccion_combobox = ttk.Combobox(frame, values=opciones_seccion)
        self.seccion_combobox.set(opciones_seccion[0]) 
        self.seccion_combobox.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        Label(frame, text='Email').grid(row=2, column=2)
        self.email_entry = Entry(frame)
        self.email_entry.grid(row=2, column=3)         

        # Botones
        ttk.Button(frame, text='Registrar Estudiante', command=self.resgist_estud).grid(row=3, column=0, columnspan=4, sticky=W+E, padx=5, pady=5)
        ttk.Button(frame, text='Registrar Notas.', command=self.agregar_notas).grid(row=4, column=0, columnspan=4, sticky=W+E, padx=5, pady=5)
        
        ttk.Button(frame, text='Modificar Estudiante', command=self.modificar_estudiante).grid(row=5, column=0, columnspan=4, sticky=W+E, padx=5, pady=5)
        
        # --- NUEVO BOTÓN DE ELIMINAR ESTUDIANTE ---
        ttk.Button(frame, text='Eliminar Estudiante', command=self.eliminar_estudiante).grid(row=6, column=0, columnspan=4, sticky=W+E, padx=5, pady=5)

        btn_salir = ttk.Button(frame, text='Salir', command=self.wind.destroy)
        btn_salir.grid(row=7, column=0, columnspan=4, sticky=W+E, padx=5, pady=5)

        self.messaje = Label(frame, text='', fg='red')
        self.messaje.grid(row=8, column=0, columnspan=4, sticky=W+E)

        # Treeview principal
        self.tree=ttk.Treeview(self.wind, columns=('col0', 'col1', 'col2', 'col3','col4','col5'), show='headings')
        self.tree.grid(row=5, column=0, padx=10, pady=10, sticky="nsew")
        self.tree.heading('col0', text='Cédula', anchor=CENTER)
        self.tree.heading('col1', text='Nombre', anchor=CENTER)
        self.tree.heading('col2', text='Apellido', anchor=CENTER)
        self.tree.heading('col3', text='Nivel', anchor=CENTER)
        self.tree.heading('col4', text='Sección', anchor=CENTER)
        self.tree.heading('col5', text='Email', anchor=CENTER)
        self.tree.column('col0', width=100)
        self.tree.column('col1', width=100)
        self.tree.column('col2', width=100)
        self.tree.column('col3', width=50)
        self.tree.column('col4', width=50)
        self.tree.column('col5', width=200)
    
        self.get_estudiantes()  
    
    def run_query(self, query, parameters = ()):
        with sqlite3.connect(self.db_name) as conn:
            cursor=conn.cursor()
            result=cursor.execute(query, parameters)
            conn.commit()
        return result
    
    def get_estudiantes(self): 
        # Elimina todos los registros del Treeview para actualizarlos
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)
        
        # 'ASC' o DESC si se quiere orden descendente (decreciente)
        query = 'SELECT * FROM estudiantes ORDER BY seccion ASC, cedula_estudiante ASC'
        
        db_rows = self.run_query(query)
        for row in db_rows:
            self.tree.insert('', 'end', text=row[0], values=(row[0], row[1], row[2], row[3], row[4], row[5]))


    def validation(self):
        return (
            len(self.cedula_entry.get()) != 0 and
            len(self.nombre_entry.get()) != 0 and
            len(self.apellido_entry.get()) != 0 and
            len(self.email_entry.get()) != 0
        )
    
    def resgist_estud (self):
        if self.validation():
           query = 'INSERT INTO estudiantes VALUES (?, ?, ?, ?, ?, ?)'
           parameters= (
               self.cedula_entry.get(),
               self.nombre_entry.get(),
               self.apellido_entry.get(),
               self.nivel_combobox.get(),
               self.seccion_combobox.get(),
               self.email_entry.get()
           )
           self.run_query(query, parameters)
           self.messaje['text']= 'Estudiante {} agragado satisfactoriamente'.format(self.nombre_entry.get())
           
           self.cedula_entry.delete(0, END)
           self.nombre_entry.delete(0, END)
           self.apellido_entry.delete(0, END)
           self.email_entry.delete(0, END)
        else:
            self.messaje['text']= 'Todos los campos son requeridos'
        
        self.get_estudiantes() 
        
    def agregar_notas(self):     
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showwarning("Error", "Debe seleccionar un estudiante para agregar notas.")
            return

        values = self.tree.item(selected_item, 'values')
        cedula_estudiante = values[0]  
        
        VentanaNotas(self.wind, cedula_estudiante)

    def modificar_estudiante(self):
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showwarning("Error", "Debe seleccionar un estudiante para modificar.")
            return

        values = self.tree.item(selected_item, 'values')
        estudiante_data = {
            'cedula': values[0],
            'nombre': values[1],
            'apellido': values[2],
            'nivel': values[3],
            'seccion': values[4],
            'email': values[5]
        }
        
        VentanaModificar(self.wind, estudiante_data, self)

    def eliminar_estudiante(self):
        self.messaje['text'] = ''
        try:
            selected_item = self.tree.selection()
            if not selected_item:
                messagebox.showwarning("Error", "Debe seleccionar un estudiante para eliminar.")
                return

            cedula_a_eliminar = self.tree.item(selected_item, 'text')
            
            # Mensaje de confirmación
            respuesta = messagebox.askyesno(
                "Confirmar Eliminación", 
                f"¿Está seguro de que desea eliminar al estudiante con cédula {cedula_a_eliminar}?"
            )
            
            if respuesta:
                # Eliminar de la tabla de estudiantes
                query = 'DELETE FROM estudiantes WHERE cedula_estudiante = ?'
                self.run_query(query, (cedula_a_eliminar,))
                
                # Eliminar de la tabla de notas (si existe)
                query_notas = 'DELETE FROM notas WHERE cedula_estudiante = ?'
                self.run_query(query_notas, (cedula_a_eliminar,))
                
                self.messaje['text'] = f'Estudiante con cédula {cedula_a_eliminar} eliminado correctamente.'
                self.get_estudiantes()
        except Exception as e:
            self.messaje['text'] = f'Error al eliminar el estudiante: {e}'

if __name__ == '__main__':
    window = Tk()
    apliclation = Control(window) 
    window.mainloop()


   #    python3 index2.py
   #    python3 -m venv venv
   #    source venv/bin/activate
   #    deactivate
    #   git push origin master


