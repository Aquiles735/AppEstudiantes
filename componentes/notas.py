import tkinter as tk
from tkinter import ttk
import sqlite3
from tkinter import messagebox

class VentanaNotas:
    db_name = 'registro_estudiante.db'

    def __init__(self, master, cedula_estudiante=None, callback_actualizar=None):
        self.registrar_notas = tk.Toplevel(master)
        self.registrar_notas.title("Registrar Notas")
        
        self.callback_actualizar = callback_actualizar
        
        # Llama a la función para inicializar la tabla de notas para todos los estudiantes
        self.inicializar_tabla_notas()
        
        contenedor_widgets = ttk.Frame(self.registrar_notas)
        contenedor_widgets.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.message = tk.Label(contenedor_widgets, text='', fg='red')
        self.message.grid(row=6, column=0, columnspan=2, sticky='ew')

        tk.Label(contenedor_widgets, text='Cédula:').grid(row=0, column=0, pady=5, padx=5, sticky="e")
        self.cedula_entry = tk.Entry(contenedor_widgets)
        self.cedula_entry.grid(row=0, column=1, pady=5, padx=5, sticky="w")
        self.cedula_entry.focus()
        
        if cedula_estudiante:
            self.cedula_entry.insert(0, cedula_estudiante)
            self.cedula_entry.config(state='readonly')
        
        tk.Label(contenedor_widgets, text='Evaluacion:').grid(row=1, column=0, pady=5, padx=5, sticky="e")
        opciones_evaluacion = ['evaluacion_1','evaluacion_2','evaluacion_3','evaluacion_4','evaluacion_5','evaluacion_6','evaluacion_7','evaluacion_8','evaluacion_9','evaluacion_10']
        self.combobox_opciones_eval = ttk.Combobox(contenedor_widgets, values=opciones_evaluacion, state='readonly')
        self.combobox_opciones_eval.set(opciones_evaluacion[0]) 
        self.combobox_opciones_eval.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        tk.Label(contenedor_widgets, text='Nota:').grid(row=2, column=0, pady=5, padx=5, sticky="e")
        self.nota_entry = tk.Entry(contenedor_widgets)
        self.nota_entry.grid(row=2, column=1, pady=5, padx=5, sticky="w")

        tk.Label(contenedor_widgets, text='Número de Evaluaciones:').grid(row=3, column=0, pady=5, padx=5, sticky="e")
        opciones_evaluaciones = ['1','2','3','4','5','6','7','8','9', '10']
        self.combobox_num_evaluaciones = ttk.Combobox(contenedor_widgets, values=opciones_evaluaciones, state='readonly')
        self.combobox_num_evaluaciones.set(opciones_evaluaciones[0]) 
        self.combobox_num_evaluaciones.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

        btn_registrar = ttk.Button(contenedor_widgets, text='Guardar Nota', command=self.guardar_nota)
        btn_registrar.grid(row=4, column=1, pady=10, sticky="we")
        btn_registrar.bind('<Return>', lambda event=None: self.guardar_nota())
       
        btn_actualizar_promedios = ttk.Button(contenedor_widgets, text='Actualizar Promedios', command=self.actualizar_promedios)
        btn_actualizar_promedios.grid(row=5, column=1, pady=10, sticky="we")
        btn_actualizar_promedios.bind('<Return>', lambda event=None: self.actualizar_promedios())

        btn_salir = ttk.Button(contenedor_widgets, text='Salir', command=self.registrar_notas.destroy)
        btn_salir.grid(row=5, column=2, pady=10, padx=(5,0), sticky="we")
        btn_salir.bind('<Return>', lambda event=None: self.registrar_notas.destroy())

        self.tree = ttk.Treeview(self.registrar_notas, columns=('col1', 'col2','col3','col4','col5','col6','col7','col8','col9','col10','col11','col12','col13'), show='headings')
        self.tree.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

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
        self.tree.column('col12', width=100)
        self.tree.column('col13', width=100)

        self.get_notes()  

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
                   
        # Consulta para traer todas las notas, sin filtrar por cédula
        query ='SELECT cedula_estudiante, evaluacion_1, evaluacion_2, evaluacion_3, evaluacion_4, evaluacion_5, evaluacion_6, evaluacion_7,evaluacion_8,evaluacion_9,evaluacion_10, promedio_notas, nota_definitiva FROM notas'
        
        db_rows = self.run_query(query)
        for row in db_rows:
            self.tree.insert('', 'end', text=row[0], values=row[0:])

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
            self.message['text'] = f'Nota guardada para la cédula {cedula}.'
            
            self.get_notes()
            
            if self.callback_actualizar:
                self.callback_actualizar()
            
            self.nota_entry.delete(0, 'end')

        except ValueError:
            self.message['text'] = 'La nota debe ser un número válido.'
        except Exception as e:
            self.message['text'] = f'Error al guardar la nota: {e}'

    def actualizar_promedios(self):
        try:
            num_evaluaciones_str = self.combobox_num_evaluaciones.get()
            
            try:
                num_evaluaciones = int(num_evaluaciones_str)
                if num_evaluaciones <= 0:
                    self.message['text'] = 'El número de evaluaciones debe ser mayor a 0.'
                    return
            except ValueError:
                self.message['text'] = 'El número de evaluaciones debe ser un número entero válido.'
                return

            update_query = f"""
            UPDATE notas
            SET 
                promedio_notas = ROUND(
                    (
                        COALESCE(evaluacion_1, 0) +
                        COALESCE(evaluacion_2, 0) +
                        COALESCE(evaluacion_3, 0) +
                        COALESCE(evaluacion_4, 0) +
                        COALESCE(evaluacion_5, 0) +
                        COALESCE(evaluacion_6, 0) +
                        COALESCE(evaluacion_7, 0) +
                        COALESCE(evaluacion_8, 0) +
                        COALESCE(evaluacion_9, 0) +
                        COALESCE(evaluacion_10, 0) 
                        
                    ) * 1.0 / {num_evaluaciones},
                    2
                ),
                nota_definitiva = ROUND(
                    (
                        COALESCE(evaluacion_1, 0) +
                        COALESCE(evaluacion_2, 0) +
                        COALESCE(evaluacion_3, 0) +
                        COALESCE(evaluacion_4, 0) +
                        COALESCE(evaluacion_5, 0) +
                        COALESCE(evaluacion_6, 0) +
                        COALESCE(evaluacion_7, 0) +
                        COALESCE(evaluacion_8, 0) +
                        COALESCE(evaluacion_9, 0) +
                        COALESCE(evaluacion_10, 0) 
                    ) * 1.0 / {num_evaluaciones},
                    0
                );
            """
            self.run_query(update_query)

            self.message['text'] = f'Actualizado promedios y totales usando {num_evaluaciones} evaluaciones.'
            
            self.get_notes()
            
            if self.callback_actualizar:
                self.callback_actualizar()

        except Exception as e:
            self.message['text'] = f'Error al actualizar promedios: {e}'

