import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkinter import *
import sqlite3
import os
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment

# Importa las clases de las otras ventanas
from componentes.notas import VentanaNotas
from componentes.modifica import VentanaModificar

class Control:
    db_name = 'registro_estudiante.db'

    def __init__(self, window):
        self.wind = window
        self.wind.title('Sistema de Registro de Estudiantes (Elab: Prof.Aquiles M. 08/2025)')
        self.wind.geometry('1200x700')
        self.wind.config(bg='#2c3e50') 
        
        self.style = ttk.Style()
        self.style.theme_use('clam') # Un tema base que es fácil de modificar

        # Estilo para el Frame principal
        self.style.configure(
            'TFrame',
            background='#34495e',
            bordercolor='#2c3e50',
            borderwidth=5
        )

        # Estilo para las etiquetas
        self.style.configure(
            'TLabel',
            background='#34495e',
            foreground='#ecf0f1',
            font=('Helvetica', 10)
        )
        

        self.style.configure(
            'TButton',
            background='#3498db', # Azul original
            foreground='white',
            font=('Helvetica', 12, 'bold'),
            borderwidth=1
        )
        self.style.map(
            'TButton',
            background=[('active', '#2980b9')], 
            foreground=[('focus', '#7de918')],
            bordercolor=[('focus', '#7de918')]
        )
        
        # Nuevo estilo para los botones rojos
        self.style.configure(
            'Red.TButton',
            background='#e74c3c',
            foreground='white',
            font=('Helvetica', 10, 'bold'),
            borderwidth=1
        )
        self.style.map(
            'Red.TButton',
            background=[('active', '#c0392b')],
            foreground=[('focus', 'white')],
            bordercolor=[('focus', '#7de918')]
        )

        
        # Estilo para los Entry (campos de texto)
        self.style.configure(
            'TEntry',
            fieldbackground='#ecf0f1',
            foreground='#2c3e50',
            font=('Helvetica', 10)
        )
        
        # Estilo para los Combobox
        self.style.configure(
            'TCombobox',
            fieldbackground='#ecf0f1',
            foreground='#2c3e50',
            font=('Helvetica', 10)
        )

        # Estilo para el Treeview
        self.style.configure(
            'Treeview',
            background='#ecf0f1',
            foreground='#2c3e50',
            rowheight=25,
            fieldbackground='#ecf0f1',
            font=('Helvetica', 10)
        )
        self.style.configure(
            'Treeview.Heading',
            background='#34495e',
            foreground='white',
            font=('Helvetica', 10, 'bold')
        )
        self.style.map(
            'Treeview',
            background=[('selected', '#3498db')] # Resalta la fila seleccionada
        )


        # --- Widgets de la ventana principal ---
        main_container = tk.Frame(self.wind, bg='#2c3e50')
        main_container.pack(fill='both', expand=True, padx=10, pady=10)
        
        frame = LabelFrame(main_container, text='Registro de Estudiantes', bg='#34495e', fg='white', font=('Helvetica', 12, 'bold'))
        frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        main_container.grid_columnconfigure(0, weight=2)
        main_container.grid_columnconfigure(1, weight=1)

        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=1)
        frame.grid_columnconfigure(2, weight=1)
        frame.grid_columnconfigure(3, weight=1)

        Label(frame, text='Cédula', bg='#34495e', fg='#ecf0f1').grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.cedula_entry = ttk.Entry(frame)
        self.cedula_entry.grid(row=0, column=1, padx=5, pady=5, sticky='ew')

        Label(frame, text='Nombre:', bg='#34495e', fg='#ecf0f1').grid(row=0, column=2, padx=5, pady=5, sticky='e')
        self.nombre_entry = ttk.Entry(frame)
        self.nombre_entry.grid(row=0, column=3, padx=5, pady=5, sticky='ew')

        Label(frame, text='Apellido:', bg='#34495e', fg='#ecf0f1').grid(row=1, column=0, padx=5, pady=5, sticky='e')
        self.apellido_entry = ttk.Entry(frame)
        self.apellido_entry.grid(row=1, column=1, padx=5, pady=5, sticky='ew')


        Label(frame, text='Nivel:', bg='#34495e', fg='#ecf0f1').grid(row=1, column=2, padx=5, pady=5, sticky='e')
        opciones_nivel = ['1 año', '2 año', '3 año', '4 año', '5 año','6 año']
        self.nivel_combobox = ttk.Combobox(frame, values=opciones_nivel)
        self.nivel_combobox.set(opciones_nivel[0]) 
        self.nivel_combobox.grid(row=1, column=3, padx=5, pady=5, sticky="ew")

        Label(frame, text='Sección:', bg='#34495e', fg='#ecf0f1').grid(row=2, column=0, padx=5, pady=5, sticky='e')
        opciones_seccion = ['A','B','C','D','E','F','G','H']
        self.seccion_combobox = ttk.Combobox(frame, values=opciones_seccion)
        self.seccion_combobox.set(opciones_seccion[0]) 
        self.seccion_combobox.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        Label(frame, text='Email:', bg='#34495e', fg='#ecf0f1').grid(row=2, column=2, padx=5, pady=5, sticky='e')
        self.email_entry = ttk.Entry(frame)
        self.email_entry.grid(row=2, column=3, padx=5, pady=5, sticky='ew')

       # botones
        btn_registrar = ttk.Button(frame, text='Registrar Estudiante', command=self.resgist_estud)
        btn_registrar.grid(row=3, column=0, columnspan=4, sticky='we', padx=5, pady=10)
        btn_registrar.bind('<Return>', lambda event: btn_registrar.invoke())
        Label(frame, text='Seleccionar un estudiante para registrar o modificar nota', bg='#34495e', fg="#7de918").grid(row=4, column=0, columnspan=4, sticky='we', padx=5, pady=(10,0))
        
        btn_notas = ttk.Button(frame, text='Registrar Notas', command=self.agregar_notas)
        btn_notas.grid(row=5, column=0, columnspan=4, sticky='we', padx=100, pady= 10)
        btn_notas.bind('<Return>', lambda event: btn_notas.invoke())
        Label(frame, text='Seleccionar un estudiante para modificar Datos ( excepto Cédula de identidad)', bg='#34495e', fg='#7de918').grid(row=6, column=0, columnspan=4, sticky='we', padx=5, pady=(10,0))
        
        btn_modificar = ttk.Button(frame, text='Modificar datos de Estudiante', command=self.modificar_estudiante)
        btn_modificar.grid(row=7, column=0, columnspan=4, sticky='we', padx=100, pady=10)
        btn_modificar.bind('<Return>', lambda event: btn_modificar.invoke())
        Label(frame, text='Seleccionar un estudiante para retirarlo del registro', bg='#34495e', fg='#7de918').grid(row=8, column=0,columnspan=4, sticky='we', padx=100, pady=(10,0))
        
        btn_eliminar = ttk.Button(frame, text='Eliminar Estudiante', command=self.eliminar_estudiante)
        btn_eliminar.grid(row=9, column=0, columnspan=4, sticky='we', padx=100, pady=10)
        btn_eliminar.bind('<Return>', lambda event: btn_eliminar.invoke())
        Label(frame, text='Seleccionar un estudiante para descargar en EXCEL las notas de la sección ', bg='#34495e', fg='#7de918').grid(row=10, column=0, columnspan=4, sticky='we', padx=5, pady=(10,0))
        
        btn_descargar = ttk.Button(frame, text='Descargar Notas en EXCEL', command=self.descargar_notas_a_excel)
        btn_descargar.grid(row=12, column=0, columnspan=4, sticky='we', padx=150, pady=(10,0))
        btn_descargar.bind('<Return>', lambda event: btn_descargar.invoke())
        
        btn_salir = ttk.Button(frame, text='Salir', command=self.wind.destroy)
        btn_salir.grid(row=14, column=0, columnspan=4, sticky='we', padx=200, pady=10)
        btn_salir.bind('<Return>', lambda event: btn_salir.invoke())
        
        self.messaje = Label(frame, text='', bg='#34495e', fg='#e74c3c', font=('Helvetica', 10, 'bold')) # Rojo oscuro para errores
        self.messaje.grid(row=13, column=0, columnspan=4, sticky='we')

        
        self.tree=ttk.Treeview(main_container, columns=('col0', 'col1', 'col2', 'col3','col4','col5'), show='headings')
        self.tree.grid(row=0, column=1, padx=10, pady=10, sticky="nsew") # Ajusta la posición del Treeview

        # Scrollbar para el Treeview
        scrollbar = ttk.Scrollbar(main_container, orient="vertical", command=self.tree.yview)
        scrollbar.grid(row=0, column=2, sticky='ns')
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Define el peso de las filas y columnas para que la ventana se ajuste
        main_container.grid_rowconfigure(0, weight=1)
        
        self.tree.heading('col0', text='Cédula', anchor=CENTER)
        self.tree.heading('col1', text='Nombre', anchor=CENTER)
        self.tree.heading('col2', text='Apellido', anchor=CENTER)
        self.tree.heading('col3', text='Nivel', anchor=CENTER)
        self.tree.heading('col4', text='Secc', anchor=CENTER)
        self.tree.heading('col5', text='Email', anchor=CENTER)
        self.tree.column('col0', width=100)
        self.tree.column('col1', width=100)
        self.tree.column('col2', width=100)
        self.tree.column('col3', width=50)
        self.tree.column('col4', width=50)
        self.tree.column('col5', width=200)



         # Frame para los nuevos botones
        botones_frame = tk.Frame(self.wind, bg='#2c3e50')
        botones_frame.pack(side='bottom', fill='x', padx=10, pady=10)
        
        # Asigna el nuevo estilo 'Red.TButton' a estos dos botones
        self.borrar_todo_btn = ttk.Button(botones_frame, text="Borrar todos los estudiantes y notas", style='Red.TButton', command=self.borrar_todo, takefocus=0)
        self.borrar_todo_btn.pack(side='right', padx=5)

        self.borrar_notas_btn = ttk.Button(botones_frame, text="Borrar todas las notas", style='Red.TButton', command=self.borrar_todas_las_notas, takefocus=0)
        self.borrar_notas_btn.pack(side='right', padx=5)


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

    #  LA LÓGICA DE VALIDACIÓN ---
    def validation(self):
        """
        Valida que los campos requeridos cumplan con el formato.
        - Cédula: solo números, sin puntos ni separaciones.
        - Nombre y Apellido: no vacíos y con la primera letra en mayúscula.
        """
        self.messaje['text'] = '' # Limpia el mensaje de error
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

    #  VALIDACIÓN ---
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
            self.messaje.config(fg='#2ecc71') # Cambia el color a verde para éxito
            self.messaje['text']= f'Estudiante {self.nombre_entry.get()} agregado satisfactoriamente'
            
            # Limpiar los campos después de un registro exitoso
            self.cedula_entry.delete(0, END)
            self.nombre_entry.delete(0, END)
            self.apellido_entry.delete(0, END)
            self.email_entry.delete(0, END)
        else:
            self.messaje.config(fg='#e74c3c') # Color rojo para errores
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

                self.messaje.config(fg='#2ecc71')
                self.messaje['text'] = f'Estudiante con cédula {cedula_a_eliminar} eliminado correctamente.'
                self.get_estudiantes()
        except Exception as e:
            self.messaje.config(fg='#e74c3c')
            self.messaje['text'] = f'Error al eliminar el estudiante: {e}'

    # --- FUNCIÓN PARA DESCARGAR NOTAS A EXCEL (con los cambios aplicados) ---
    def descargar_notas_a_excel(self):
        """Descarga los datos de los estudiantes y sus notas a un archivo de Excel."""
        try:
            selected_item = self.tree.focus()
            if not selected_item:
                messagebox.showwarning("Error", "Debe seleccionar un estudiante para descargar notas de la sección.")
                return

            values = self.tree.item(selected_item, 'values')
            if not values:
                messagebox.showwarning("Error", "Los datos del estudiante seleccionado no son válidos.")
                return

            nivel_seleccionado = values[3]
            seccion_seleccionada = values[4]
            
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
                'Promedio', 'TOTAL'
            ]
            ws.append(headers)
            
            # Estilo de los encabezados (se dejan centrados)
            for col in range(1, len(headers) + 1):
                cell = ws.cell(row=1, column=col)
                cell.font = Font(bold=True)
                cell.alignment = Alignment(horizontal='center', vertical='center')

            # 4. Escribir los datos en el archivo y aplicar la alineación
            row_number = 2
            for row in data_rows:
                ws.append(row)
                
                # Alinear a la izquierda las columnas numéricas (de F a Q)
                # que corresponden a los índices de columna del 6 al 17
                for col_index in range(6, 18):
                    cell_to_align = ws.cell(row=row_number, column=col_index)
                    cell_to_align.alignment = Alignment(horizontal='left', vertical='center')

                row_number += 1
            
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

    def borrar_todas_las_notas(self):
        """Borra todas las notas de todos los estudiantes."""
        respuesta = messagebox.askyesno(
            "Confirmar",
            "¿Está seguro de que desea borrar todas las notas de todos los estudiantes? Esta acción es irreversible."
        )
        if respuesta:
            query = 'DELETE FROM notas'
            self.run_query(query)
            messagebox.showinfo("Éxito", "Todas las notas han sido borradas correctamente.")
            self.get_estudiantes() # Actualiza la vista si es necesario

    def borrar_todo(self):
        """Borra todos los estudiantes y sus notas."""
        respuesta = messagebox.askyesno(
            "Confirmar",
            "ADVERTENCIA: ¿Está seguro de que desea borrar TODOS los estudiantes y TODAS sus notas? Esta acción es irreversible."
        )
        if respuesta:
            query_estudiantes = 'DELETE FROM estudiantes'
            self.run_query(query_estudiantes)
            query_notas = 'DELETE FROM notas'
            self.run_query(query_notas)
            messagebox.showinfo("Éxito", "Todos los estudiantes y sus notas han sido borrados correctamente.")
            self.get_estudiantes() # Actualiza la vista


if __name__ == '__main__':
    window = Tk()
    application = Control(window)
    window.mainloop()


    # mis anotaciones de mergencia por cambio linux----window A.M.
   #    python3 index2.py
   #    python3 -m venv venv     linux
   #    source venv/bin/activate    linux
   #    deactivate
   #   git checkout main     <para cambiar de rama a main>  o
   #   git checkout master
   #   git push origin HEAD     para push en master github
   #                                git pull origin master
   #     pyinstaller index2.py   pyinstaller --onefile index2.py 
   #AppAcademi/dist/index2 AppAcademi/dist/registro_estudiante.db
#      pyinstaller --onefile --noconsole index2.py
  #   /home/aquiles/Documentos/MiAcademi/AppAcademi/venv/bin/python

