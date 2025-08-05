import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkinter import *
import sqlite3
import os
import openpyxl
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment

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
        opciones_nivel = ['1 año', '2 año', '3 año', '4 año', '5 año','6 año']
        self.nivel_combobox = ttk.Combobox(frame, values=opciones_nivel)
        self.nivel_combobox.set(opciones_nivel[0]) 
        self.nivel_combobox.grid(row=1, column=3, padx=5, pady=5, sticky="ew")

        Label(frame, text='Seccion').grid(row=2, column=0)
        opciones_seccion = ['A','B','C','D','E','F','G','H']
        self.seccion_combobox = ttk.Combobox(frame, values=opciones_seccion)
        self.seccion_combobox.set(opciones_seccion[0]) 
        self.seccion_combobox.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        Label(frame, text='Email').grid(row=2, column=2)
        self.email_entry = Entry(frame)
        self.email_entry.grid(row=2, column=3)    

        # Botones y se activan con ENTER
        btn_registrar = ttk.Button(frame, text='Registrar Estudiante', command=self.resgist_estud)
        btn_registrar.grid(row=3, column=0, columnspan=4, sticky='we', padx=5, pady=5)
        btn_registrar.bind('<Return>', lambda event: btn_registrar.invoke())

        btn_notas = ttk.Button(frame, text='Registrar Notas', command=self.agregar_notas)
        btn_notas.grid(row=4, column=0, columnspan=4, sticky='we', padx=5, pady=5)
        btn_notas.bind('<Return>', lambda event: btn_notas.invoke())

        btn_modificar = ttk.Button(frame, text='Modificar Estudiante', command=self.modificar_estudiante)
        btn_modificar.grid(row=5, column=0, columnspan=4, sticky='we', padx=5, pady=5)
        btn_modificar.bind('<Return>', lambda event: btn_modificar.invoke())

        btn_eliminar = ttk.Button(frame, text='Eliminar Estudiante', command=self.eliminar_estudiante)
        btn_eliminar.grid(row=6, column=0, columnspan=4, sticky='we', padx=5, pady=5)
        btn_eliminar.bind('<Return>', lambda event: btn_eliminar.invoke())
       
        btn_salir = ttk.Button(frame, text='Salir', command=self.wind.destroy)
        btn_salir.grid(row=7, column=0, columnspan=2, sticky='we', padx=5, pady=5)
        btn_salir.bind('<Return>', lambda event: btn_salir.invoke())
        
        # --- NUEVO BOTÓN: DESCARGAR NOTAS ---
        btn_descargar = ttk.Button(frame, text='Descargar Notas', command=self.descargar_notas_a_excel)
        btn_descargar.grid(row=7, column=2, columnspan=2, sticky='we', padx=5, pady=5)
        btn_descargar.bind('<Return>', lambda event: btn_descargar.invoke())
        
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
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)
        
        query = 'SELECT * FROM estudiantes ORDER BY nivel ASC, seccion ASC, CAST(cedula_estudiante AS INTEGER) ASC;'
        
        db_rows = self.run_query(query)
        for row in db_rows:
            self.tree.insert('', 'end', text=row[0], values=row[0:])

    # --- MÉTODO 'validation' ACTUALIZADO CON LA LÓGICA DE VALIDACIÓN ---
    def validation(self):
        """
        Valida que los campos requeridos cumplan con el formato.
        - Cédula: solo números, sin puntos ni separaciones.
        - Nombre y Apellido: no vacíos y con la primera letra en mayúscula.
        """
        cedula = self.cedula_entry.get()
        nombre = self.nombre_entry.get()
        apellido = self.apellido_entry.get()
        email = self.email_entry.get()

        if not cedula.isdigit():
            self.messaje['text'] = 'La Cédula debe contener solo números.'
            return False

        if not nombre or not apellido or not email:
            self.messaje['text'] = 'Todos los campos son requeridos.'
            return False

        if not nombre.istitle():
            self.messaje['text'] = 'El Nombre debe comenzar con mayúscula.'
            return False

        if not apellido.istitle():
            self.messaje['text'] = 'El Apellido debe comenzar con mayúscula.'
            return False
            
        # Si todas las validaciones pasan
        return True
    
    # --- MÉTODO 'resgist_estud' ACTUALIZADO PARA USAR LA NUEVA VALIDACIÓN ---
    def resgist_estud(self):
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
           self.messaje['text']= f'Estudiante {self.nombre_entry.get()} agregado satisfactoriamente'
           
           # Limpiar los campos después de un registro exitoso
           self.cedula_entry.delete(0, END)
           self.nombre_entry.delete(0, END)
           self.apellido_entry.delete(0, END)
           self.email_entry.delete(0, END)
        else:
           # El mensaje de error ya se ha establecido en el método validation()
           pass
        
        self.get_estudiantes() 

    def agregar_notas(self):     
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showwarning("Error", "Debe seleccionar un estudiante para agregar notas.")
            return
        values = self.tree.item(selected_item, 'values')
        if values:
            datos_estudiante = {
                'cedula_estudiante': values[0],
                'nivel_estudiante': values[3],
                'seccion_estudiante': values[4]
            }
            VentanaNotas(self.wind, **datos_estudiante, callback_actualizar=self.get_estudiantes)

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
            
            respuesta = messagebox.askyesno(
                "Confirmar Eliminación", 
                f"¿Está seguro de que desea eliminar al estudiante con cédula {cedula_a_eliminar}?"
            )
            
            if respuesta:
                query = 'DELETE FROM estudiantes WHERE cedula_estudiante = ?'
                self.run_query(query, (cedula_a_eliminar,))
                
                query_notas = 'DELETE FROM notas WHERE cedula_estudiante = ?'
                self.run_query(query_notas, (cedula_a_eliminar,))
                
                self.messaje['text'] = f'Estudiante con cédula {cedula_a_eliminar} eliminado correctamente.'
                self.get_estudiantes()
        except Exception as e:
            self.messaje['text'] = f'Error al eliminar el estudiante: {e}'
    
    # --- FUNCIÓN PARA DESCARGAR NOTAS A EXCEL ---
    def descargar_notas_a_excel(self):
        """Descarga los datos de los estudiantes y sus notas a un archivo de Excel."""
        try:
            # --- NUEVO CÓDIGO: Obtener los datos del estudiante seleccionado ---
            selected_item = self.tree.focus()
            if not selected_item:
                messagebox.showwarning("Error", "Debe seleccionar un estudiante para descargar notas.")
                return

            values = self.tree.item(selected_item, 'values')
            if not values:
                messagebox.showwarning("Error", "Los datos del estudiante seleccionado no son válidos.")
                return
            
            nivel_seleccionado = values[3]
            seccion_seleccionada = values[4]
            # --- FIN DEL CÓDIGO NUEVO ---

            # 1. Realizar una consulta para obtener los datos combinados
            query = """
            SELECT 
                e.cedula_estudiante, e.nombre, e.apellido, e.nivel, e.seccion,
                n.evaluacion_1, n.evaluacion_2, n.evaluacion_3, n.evaluacion_4, n.evaluacion_5,
                n.evaluacion_6, n.evaluacion_7, n.evaluacion_8, n.evaluacion_9, n.evaluacion_10,
                n.promedio_notas, n.nota_definitiva
            FROM estudiantes e
            INNER JOIN notas n ON e.cedula_estudiante = n.cedula_estudiante
            WHERE e.nivel = ? AND e.seccion = ?
            ORDER BY e.nivel ASC, e.seccion ASC, CAST(e.cedula_estudiante AS INTEGER) ASC;
            """
            # --- CORRECCIÓN AQUÍ: Pasar los parámetros a run_query ---
            parameters = (nivel_seleccionado, seccion_seleccionada)
            data_rows = self.run_query(query, parameters).fetchall()

            if not data_rows:
                messagebox.showinfo("Información", "No hay datos para descargar para el nivel y sección seleccionados.")
                return

            # 2. Crear un nuevo libro de Excel y seleccionar la hoja de trabajo
            wb = Workbook()
            ws = wb.active
            ws.title = f"Notas {nivel_seleccionado} {seccion_seleccionada}"

            # 3. Definir los encabezados de las columnas
            headers = [
                'Cédula', 'Nombre', 'Apellido', 'Nivel', 'Sección',
                'Eval 1', 'Eval 2', 'Eval 3', 'Eval 4', 'Eval 5',
                'Eval 6', 'Eval 7', 'Eval 8', 'Eval 9', 'Eval 10',
                'Promedio', 'Nota Definitiva'
            ]
            ws.append(headers)
            
            # Estilo de los encabezados
            for col in range(1, len(headers) + 1):
                cell = ws.cell(row=1, column=col)
                cell.font = Font(bold=True)
                cell.alignment = Alignment(horizontal='center', vertical='center')
            
            # 4. Escribir los datos en el archivo
            for row in data_rows:
                ws.append(row)

            # 5. Ajustar el ancho de las columnas
            for col in ws.columns:
                max_length = 0
                column = col[0].column_letter
                for cell in col:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except:
                        pass
                adjusted_width = (max_length + 2)
                ws.column_dimensions[column].width = adjusted_width

            # 6. Guardar el archivo
            filename = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Archivos de Excel", "*.xlsx")],
                title="Guardar como",
                initialfile=f"Notas_{nivel_seleccionado}_{seccion_seleccionada}.xlsx"
            )
            
            if filename:
                wb.save(filename)
                messagebox.showinfo("Éxito", f"Notas guardadas exitosamente en:\n{os.path.basename(filename)}")

        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al descargar el archivo: {e}")

if __name__ == '__main__':
    window = Tk()
    apliclation = Control(window) 
    window.mainloop()


   #    python3 index2.py
   #    python3 -m venv venv
   #    source venv/bin/activate
   #    deactivate
   #   git checkout main     <para cambiar de rama a main>  o
   #   git checkout master
   #   git push origin HEAD     para push en master github
   #                                git pull origin master
   #     pyinstaller index2.py   pyinstaller --onefile index2.py 
   #AppAcademi/dist/index2 AppAcademi/dist/registro_estudiante.db
    #  ruta completa de venv
  #   /home/aquiles/Documentos/MiAcademi/AppAcademi/venv/bin/python

