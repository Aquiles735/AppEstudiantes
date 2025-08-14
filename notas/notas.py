import tkinter as tk
from tkinter import ttk
import sqlite3
from tkinter import messagebox
from notas.widgets_notas import create_widgets


class VentanaNotas(tk.Toplevel):
    db_name = "registro_estudiante.db"

    def __init__(
        self,
        master,
        cedula_estudiante=None,
        nivel_estudiante=None,
        seccion_estudiante=None,
        callback_actualizar=None,
    ):
        super().__init__(master)

        self.callback_actualizar = callback_actualizar
        self.nivel_estudiante = nivel_estudiante
        self.seccion_estudiante = seccion_estudiante

        create_widgets(self, master, cedula_estudiante)

    def inicializar_tabla_notas(self):
        query_estudiantes = "SELECT cedula_estudiante FROM estudiantes"
        estudiantes_db = self.run_query(query_estudiantes).fetchall()

        for estudiante in estudiantes_db:

            cedula = estudiante[0]
            query_check = (
                "SELECT cedula_estudiante FROM notas WHERE cedula_estudiante = ?"
            )
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
                n.cedula_estudiante, e.nombre, e.apellido, n.evaluacion_1, n.evaluacion_2, n.evaluacion_3, n.evaluacion_4, n.evaluacion_5, 
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
                n.cedula_estudiante, e.nombre, e.apellido, n.evaluacion_1, n.evaluacion_2, n.evaluacion_3, n.evaluacion_4, n.evaluacion_5, 
                n.evaluacion_6, n.evaluacion_7, n.evaluacion_8, n.evaluacion_9, n.evaluacion_10, 
                n.promedio_notas, n.nota_definitiva 
            FROM notas n
            INNER JOIN estudiantes e ON n.cedula_estudiante = e.cedula_estudiante
            ORDER BY CAST(n.cedula_estudiante AS INTEGER) ASC
            """
            parameters = ()

        db_rows = self.run_query(query, parameters)

        # Iterar sobre las filas de la base de datos
        for row in db_rows:
            row_list = list(row)

            # Formatear las notas (columnas 3 a 12)
            for i in range(3, 13):
                nota = row_list[i]
                if nota is not None:
                    # Convierte la nota a entero  con 2 dígitos
                    row_list[i] = f"{int(nota):02d}"

            # Formatear el promedio
            promedio_index = 13
            promedio = row_list[promedio_index]
            if promedio is not None:
                row_list[promedio_index] = f"{promedio:.2f}"

            # Formatear la nota definitiva
            nota_definitiva_index = 14
            nota_definitiva = row_list[nota_definitiva_index]
            if nota_definitiva is not None:
                row_list[nota_definitiva_index] = "{:02d}".format(int(nota_definitiva))

            formatted_row = tuple(row_list)
            self.tree.insert("", "end", text=formatted_row[0], values=formatted_row)

    def seleccionar_estudiante(self, event):
     
        self.messaje["text"] = ""
        selected_item = self.tree.selection()
        if not selected_item:
            return

        item = self.tree.item(selected_item[0])
        cedula = item["values"][0]

        self.cedula_entry.config(state="normal")
        self.cedula_entry.delete(0, "end")
        self.cedula_entry.insert(0, cedula)
        self.cedula_entry.config(state="readonly")
        self.nota_entry.focus()

    def validation(self):
        return self.cedula_entry.get() and self.nota_entry.get()

    def guardar_nota(self):
        if not self.validation():
            self.messaje["text"] = "Cédula y Nota son campos obligatorios."
            return

        try:
            cedula = self.cedula_entry.get()
            evaluacion = self.combobox_opciones_eval.get()

            # Se valida que la nota sea un número entero
            nota = int(self.nota_entry.get())

            if not 0 <= nota <= 20:
                self.messaje.config(fg="#e74c3c")
                self.messaje["text"] = (
                    "La nota debe ser un número entero entre 00 y 20."
                )
                return

            query = f"UPDATE notas SET {evaluacion} = ? WHERE cedula_estudiante = ?"
            parameters = (nota, cedula)

            self.run_query(query, parameters)
            self.messaje.config(fg="#2ecc71")
            self.messaje["text"] = f'Nota guardada, presionar "Actualizar Promedios"'

            self.get_notes()

            if self.callback_actualizar:
                self.callback_actualizar()

            self.nota_entry.delete(0, "end")

        except ValueError:
            self.messaje.config(fg="#e74c3c")
            self.messaje["text"] = (
                "La nota debe ser un número entero válido (sin decimales)."
            )
        except Exception as e:
            self.messaje.config(fg="#e74c3c")
            self.messaje["text"] = f"Error al guardar la nota: {e}"

    def actualizar_promedios(self):
       
        try:
            num_evaluaciones_str = self.combobox_num_evaluaciones.get()

            try:
                num_evaluaciones = int(num_evaluaciones_str)
                if num_evaluaciones <= 0:
                    self.messaje.config(fg="#e74c3c")
                    self.messaje["text"] = (
                        "El número de evaluaciones debe ser mayor a 0."
                    )
                    return
            except ValueError:
                self.messaje.config(fg="#e74c3c")
                self.messaje["text"] = (
                    "El número de evaluaciones debe ser un número entero válido."
                )
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

            self.messaje.config(fg="#2ecc71")
            self.messaje["text"] = (
                f"Actualizado promedios y totales ( {num_evaluaciones} evaluaciones)."
            )

            self.get_notes()

            if self.callback_actualizar:
                self.callback_actualizar()

        except Exception as e:
            self.messaje.config(fg="#e74c3c")
            self.messaje["text"] = f"Error al actualizar promedios: {e}"

    def salir_con_advertencia(self):
        """Muestra un mensaje de advertencia antes de salir."""
        respuesta = messagebox.askyesno(
            "Advertencia",
            "¿Presionaste 'Guardar cambios' y 'Actualizar Promedios' antes de salir?",
        )
        if respuesta:
            self.destroy()

