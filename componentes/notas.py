import tkinter as tk
from tkinter import ttk
import sqlite3
from tkinter import messagebox

class VentanaNotas(tk.Toplevel):
    db_name = 'registro_estudiante.db'

    def __init__(self, master, cedula_estudiante=None, nivel_estudiante=None, seccion_estudiante=None, callback_actualizar=None):
        # Usamos super() para inicializar la clase Toplevel
        super().__init__(master)
        self.title("Registrar Notas")
        self.transient(master)  # Hace que esta ventana sea modal
        self.grab_set()
        self.resizable(False, False)
        self.config(bg='#34495e')
        
        self.callback_actualizar = callback_actualizar
        
        self.nivel_estudiante = nivel_estudiante
        self.seccion_estudiante = seccion_estudiante
        
        # Estilos de ttk para esta ventana
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TFrame', background='#34495e')
        style.configure('TLabel', background='#34495e', foreground='#ecf0f1', font=('Helvetica', 10))
        style.configure('TEntry', fieldbackground='#ecf0f1', foreground='#2c3e50', font=('Helvetica', 10))
        style.configure('TCombobox', fieldbackground='#ecf0f1', foreground='#2c3e50', font=('Helvetica', 10))
        style.configure('TButton', background='#3498db', foreground='white', font=('Helvetica', 10, 'bold'), borderwidth=1)
        style.map('TButton', background=[('active', '#2980b9')])
        style.configure('Treeview', background='#ecf0f1', foreground='#2c3e50', rowheight=25, fieldbackground='#ecf0f1', font=('Helvetica', 10))
        style.configure('Treeview.Heading', background='#34495e', foreground='white', font=('Helvetica', 10, 'bold'))
        style.map('Treeview', background=[('selected', '#3498db')])
        
        self.inicializar_tabla_notas()
        
        # Frame para los controles de entrada
        contenedor_widgets = ttk.Frame(self)
        contenedor_widgets.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        # Mensaje de error/éxito
        self.message = tk.Label(contenedor_widgets, text='', bg='#34495e', fg='#e74c3c', font=('Helvetica', 10, 'bold'))
        self.message.grid(row=6, column=0, columnspan=2, sticky='ew', pady=5)

        # Labels y Entries para la entrada de notas
        ttk.Label(contenedor_widgets, text='Cédula:').grid(row=0, column=0, pady=5, padx=5, sticky="e")
        self.cedula_entry = ttk.Entry(contenedor_widgets)
        self.cedula_entry.grid(row=0, column=1, pady=5, padx=5, sticky="ew")
        
        if cedula_estudiante:
            self.cedula_entry.insert(0, cedula_estudiante)
            self.cedula_entry.config(state='readonly')
        else:
            self.cedula_entry.focus()
        
        ttk.Label(contenedor_widgets, text='Evaluación:').grid(row=1, column=0, pady=5, padx=5, sticky="e")
        opciones_evaluacion = ['evaluacion_1','evaluacion_2','evaluacion_3','evaluacion_4','evaluacion_5','evaluacion_6','evaluacion_7','evaluacion_8','evaluacion_9','evaluacion_10']
        self.combobox_opciones_eval = ttk.Combobox(contenedor_widgets, values=opciones_evaluacion, state='readonly')
        self.combobox_opciones_eval.set(opciones_evaluacion[0]) 
        self.combobox_opciones_eval.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(contenedor_widgets, text='Nota:').grid(row=2, column=0, pady=5, padx=5, sticky="e")
        self.nota_entry = ttk.Entry(contenedor_widgets)
        self.nota_entry.grid(row=2, column=1, pady=5, padx=5, sticky="ew")

        ttk.Label(contenedor_widgets, text='Total de Evaluaciones:').grid(row=3, column=0, pady=5, padx=5, sticky="e")
        opciones_evaluaciones = ['1','2','3','4','5','6','7','8','9', '10']
        self.combobox_num_evaluaciones = ttk.Combobox(contenedor_widgets, values=opciones_evaluaciones, state='readonly')
        self.combobox_num_evaluaciones.set(opciones_evaluaciones[0]) 
        self.combobox_num_evaluaciones.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

        # Botones
        btn_registrar = ttk.Button(contenedor_widgets, text='Guardar Nota', command=self.guardar_nota)
        btn_registrar.grid(row=4, column=0, columnspan=2, pady=10, padx=5, sticky="we")
        btn_registrar.bind('<Return>', lambda event=None: self.guardar_nota())
        
        btn_actualizar_promedios = ttk.Button(contenedor_widgets, text='Actualizar Promedios', command=self.actualizar_promedios)
        btn_actualizar_promedios.grid(row=5, column=0, pady=5, padx=5, sticky="we")
        btn_actualizar_promedios.bind('<Return>', lambda event=None: self.actualizar_promedios())
        
        btn_salir = ttk.Button(contenedor_widgets, text='Salir', command=self.destroy, style='Accent.TButton')
        btn_salir.grid(row=5, column=1, pady=5, padx=5, sticky="we")
        btn_salir.bind('<Return>', lambda event=None: self.destroy())

        # Treeview
        self.tree = ttk.Treeview(self, columns=('col1', 'col2','col3','col4','col5','col6','col7','col8','col9','col10','col11','col12','col13'), show='headings')
        self.tree.grid(row=0, column=1, rowspan=2, padx=10, pady=10, sticky="nsew")
        
        # Enlazar el evento de selección del Treeview
        self.tree.bind('<<TreeviewSelect>>', self.seleccionar_estudiante)
        
        # Scrollbar para el Treeview
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        scrollbar.grid(row=0, column=2, rowspan=2, sticky='ns')
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Ajustes de columnas para que el treeview se expanda
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.tree.heading('col1', text='Cédula', anchor='center')
        self.tree.heading('col2', text='Eval 1', anchor='center')
        self.tree.heading('col3', text='Eval 2', anchor='center')
        self.tree.heading('col4', text='Eval 3', anchor='center')
        self.tree.heading('col5', text='Eval 4', anchor='center')
        self.tree.heading('col6', text='Eval 5', anchor='center')
        self.tree.heading('col7', text='Eval 6', anchor='center')
        self.tree.heading('col8', text='Eval 7', anchor='center')
        self.tree.heading('col9', text='Eval 8', anchor='center')
        self.tree.heading('col10', text='Eval 9', anchor='center')
        self.tree.heading('col11', text='Eval 10', anchor='center')
        self.tree.heading('col12', text='Promedio', anchor='center')
        self.tree.heading('col13', text='TOTAL', anchor='center')
        
        self.tree.column('col1', width=100)
        self.tree.column('col2', width=50)
        self.tree.column('col3', width=50)
        self.tree.column('col4', width=50)
        self.tree.column('col5', width=50)
        self.tree.column('col6', width=50)
        self.tree.column('col7', width=50)
        self.tree.column('col8', width=50)
        self.tree.column('col9', width=50)
        self.tree.column('col10', width=50)
        self.tree.column('col11', width=50)
        self.tree.column('col12', width=70)
        self.tree.column('col13', width=70)

        self.get_notes()  
        
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')

    def inicializar_tabla_notas(self):
        """Inicializa la tabla de notas con todos los estudiantes."""
        query_estudiantes = 'SELECT cedula_estudiante FROM estudiantes'
        estudiantes_db = self.run_query(query_estudiantes).fetchall()
        
        for estudiante in estudiantes_db:
            cedula = estudiante[0]
            query_check = 'SELECT cedula_estudiante FROM notas WHERE cedula_estudiante = ?'
            result = self.run_query(query_check, (cedula,)).fetchone()
            
            if not result:
                query_insert = """
                INSERT INTO notas (cedula_estudiante, evaluacion_1, evaluacion_2, evaluacion_3, evaluacion_4, evaluacion_5, evaluacion_6, evaluacion_7,evaluacion_8,evaluacion_9,evaluacion_10, promedio_notas, nota_definitiva)
                VALUES (?, NULL, NULL, NULL, NULL, NULL, NULL, NULL,NULL,NULL,NULL, 0.0, 0.0)
                """
                self.run_query(query_insert, (cedula,))

    def run_query(self, query, parameters=()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
        return result
    
    def get_notes(self):
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)
        
        if self.nivel_estudiante and self.seccion_estudiante:
            query = """
            SELECT 
                n.cedula_estudiante, n.evaluacion_1, n.evaluacion_2, n.evaluacion_3, n.evaluacion_4, n.evaluacion_5, 
                n.evaluacion_6, n.evaluacion_7, n.evaluacion_8, n.evaluacion_9, n.evaluacion_10, 
                n.promedio_notas, n.nota_definitiva
            FROM notas n
            INNER JOIN estudiantes e ON n.cedula_estudiante = e.cedula_estudiante
            WHERE e.nivel = ? AND e.seccion = ?
            ORDER BY CAST(n.cedula_estudiante AS INTEGER) ASC
            """
            parameters = (self.nivel_estudiante, self.seccion_estudiante)
        else:
            query = """
            SELECT 
                cedula_estudiante, evaluacion_1, evaluacion_2, evaluacion_3, evaluacion_4, evaluacion_5, 
                evaluacion_6, evaluacion_7, evaluacion_8, evaluacion_9, evaluacion_10, 
                promedio_notas, nota_definitiva 
            FROM notas
            ORDER BY CAST(cedula_estudiante AS INTEGER) ASC
            """
            parameters = ()
        
        db_rows = self.run_query(query, parameters)
        for row in db_rows:
            self.tree.insert('', 'end', text=row[0], values=row)

    def seleccionar_estudiante(self, event):
        """Carga los datos del estudiante seleccionado en los campos de entrada."""
        self.message['text'] = ''
        selected_item = self.tree.selection()
        if not selected_item:
            return
        
        # Obtener los valores de la fila seleccionada
        item = self.tree.item(selected_item[0])
        cedula = item['values'][0]
        
        # Rellenar el campo de cédula y hacerlo de solo lectura
        self.cedula_entry.config(state='normal')
        self.cedula_entry.delete(0, 'end')
        self.cedula_entry.insert(0, cedula)
        self.cedula_entry.config(state='readonly')
        self.nota_entry.focus()
        
    def validation(self):
        return self.cedula_entry.get() and self.nota_entry.get()

    def guardar_nota(self):
        if not self.validation():
            self.message['text'] = 'Cédula y Nota son campos obligatorios.'
            return
        
        try:
            cedula = self.cedula_entry.get()
            evaluacion = self.combobox_opciones_eval.get()
            nota = float(self.nota_entry.get())
            

            query = f"UPDATE notas SET {evaluacion} = ? WHERE cedula_estudiante = ?"
            parameters = (nota, cedula)
            
            self.run_query(query, parameters)
            self.message.config(fg='#2ecc71')
            self.message['text'] = f'Nota guardada para la cédula {cedula}.'
            
            self.get_notes()
            
            if self.callback_actualizar:
                self.callback_actualizar()
            
            self.nota_entry.delete(0, 'end')

        except ValueError:
            self.message.config(fg='#e74c3c')
            self.message['text'] = 'La nota debe ser un número válido.'
        except Exception as e:
            self.message.config(fg='#e74c3c')
            self.message['text'] = f'Error al guardar la nota: {e}'

    def actualizar_promedios(self):
        try:
            num_evaluaciones_str = self.combobox_num_evaluaciones.get()
            
            try:
                num_evaluaciones = int(num_evaluaciones_str)
                if num_evaluaciones <= 0:
                    self.message.config(fg='#e74c3c')
                    self.message['text'] = 'El número de evaluaciones debe ser mayor a 0.'
                    return
            except ValueError:
                self.message.config(fg='#e74c3c')
                self.message['text'] = 'El número de evaluaciones debe ser un número entero válido.'
                return

            update_query = f"""
            UPDATE notas
            SET 
                promedio_notas = ROUND(
                    (
                        COALESCE(evaluacion_1, 0) + COALESCE(evaluacion_2, 0) +
                        COALESCE(evaluacion_3, 0) + COALESCE(evaluacion_4, 0) +
                        COALESCE(evaluacion_5, 0) + COALESCE(evaluacion_6, 0) +
                        COALESCE(evaluacion_7, 0) + COALESCE(evaluacion_8, 0) +
                        COALESCE(evaluacion_9, 0) + COALESCE(evaluacion_10, 0) 
                    ) * 1.0 / {num_evaluaciones},
                    2
                ),
                nota_definitiva = ROUND(
                    (
                        COALESCE(evaluacion_1, 0) + COALESCE(evaluacion_2, 0) +
                        COALESCE(evaluacion_3, 0) + COALESCE(evaluacion_4, 0) +
                        COALESCE(evaluacion_5, 0) + COALESCE(evaluacion_6, 0) +
                        COALESCE(evaluacion_7, 0) + COALESCE(evaluacion_8, 0) +
                        COALESCE(evaluacion_9, 0) + COALESCE(evaluacion_10, 0) 
                    ) * 1.0 / {num_evaluaciones},
                    0
                )
            WHERE cedula_estudiante IN (
                SELECT cedula_estudiante FROM estudiantes WHERE nivel = ? AND seccion = ?
            );
            """
            parameters = (self.nivel_estudiante, self.seccion_estudiante)
            self.run_query(update_query, parameters)

            self.message.config(fg='#2ecc71')
            self.message['text'] = f'Actualizado promedios y totales {num_evaluaciones} evaluaciones.'
            
            self.get_notes()
            
            if self.callback_actualizar:
                self.callback_actualizar()

        except Exception as e:
            self.message.config(fg='#e74c3c')
            self.message['text'] = f'Error al actualizar promedios: {e}'




