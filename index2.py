import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sqlite3
import os
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment
from notas.notas import VentanaNotas
from modifica.modifica import VentanaModificar

from diseno import Diseno
from widgets import Widgets


class Control:
    db_name = "registro_estudiante.db"

    def __init__(self, window):
        self.wind = window
        self.wind.title(
            "Sistema de Registro de Estudiantes (Elab: Prof.Aquiles M. 08/2025)"
        )

        self.wind.geometry("1200x660")
        self.wind.config(bg="#2c3e50")

        self.diseno = Diseno(self.wind)
        self.ui = Widgets(self.wind, self)

        # Carga los estudiantes en el Treeview al iniciar
        self.get_estudiantes()

    def run_query(self, query, parameters=()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
        return result

    def get_estudiantes(self):
        records = self.ui.tree.get_children()
        for element in records:
            self.ui.tree.delete(element)

        query = "SELECT cedula_estudiante, nombre, apellido, nivel, seccion FROM estudiantes ORDER BY nivel ASC, seccion ASC, CAST(cedula_estudiante AS INTEGER) ASC;"
        db_rows = self.run_query(query)
        for row in db_rows:
            self.ui.tree.insert("", "end", text=row[0], values=row[0:])
           

    # LÓGICA DE VALIDACIÓN 
    def validation(self):
        self.ui.messaje["text"] = ""
        cedula = self.ui.cedula_entry.get()
        nombre = self.ui.nombre_entry.get()
        apellido = self.ui.apellido_entry.get()

        if not cedula.isdigit():
            self.ui.messaje["text"] = "La Cédula debe contener solo números."
            return False

        if not nombre or not apellido:
            self.ui.messaje["text"] = "Todos los campos son requeridos."
            return False

        return True
    # REGISTRAR ESTUDIANTE
    def resgist_estud(self):
        if self.validation():
            cedula_ingresada = self.ui.cedula_entry.get()

            # Obtener y formatear el nombre y el apellido para que la primera letra de cada palabra sea mayúscula

            nombre_formateado = self.ui.nombre_entry.get().title()
            apellido_formateado = self.ui.apellido_entry.get().title()

            # Revision si la cedula existe
            check_query = (
                "SELECT cedula_estudiante FROM estudiantes WHERE cedula_estudiante = ?"
            )
            existing_student = self.run_query(
                check_query, (cedula_ingresada,)
            ).fetchone()

            # Si el estudiante ya existe, muestra el error y limpia todos los campos
            if existing_student:
                self.ui.messaje.config(fg="#e74c3c")
                self.ui.messaje["text"] = (
                    "Error: Un estudiante con esa cédula ya existe."
                )
                self.ui.cedula_entry.delete(0, "end")
                self.ui.nombre_entry.delete(0, "end")
                self.ui.apellido_entry.delete(0, "end")

            else:
                # Si no existe, procede con la inserción y limpia todos los campos
                query = "INSERT INTO estudiantes VALUES (?, ?, ?, ?, ?)"
                parameters = (
                    cedula_ingresada,
                    # Usamos las variables formateadas aquí
                    nombre_formateado,
                    apellido_formateado,
                    self.ui.nivel_combobox.get(),
                    self.ui.seccion_combobox.get(),
                )
                try:
                    self.run_query(query, parameters)
                    self.ui.messaje.config(fg="#2ecc71")
                    self.ui.messaje["text"] = (
                        # Usamos el nombre formateado para el mensaje
                        f"Estudiante {nombre_formateado} agregado satisfactoriamente"
                    )
                    self.get_estudiantes()

                    # Limpia los campos después de una inserción exitosa
                    self.ui.cedula_entry.delete(0, "end")
                    self.ui.nombre_entry.delete(0, "end")
                    self.ui.apellido_entry.delete(0, "end")

                except Exception as e:
                    self.ui.messaje.config(fg="#e74c3c")
                    self.ui.messaje["text"] = f"Ocurrió un error inesperado: {e}"

        else:
            self.ui.messaje.config(fg="#e74c3c")
    

    # CARGAR DATOS EN CAMPOS DE ENTRADA 
    def seleccionar_estudiante(self, event):
        self.ui.messaje["text"] = ""
        selected_item = self.ui.tree.focus()
        if not selected_item:
            return

        item_data = self.ui.tree.item(selected_item)
        values = item_data["values"]

        self.ui.cedula_entry.config(state="normal")
        self.ui.cedula_entry.delete(0, tk.END)
        self.ui.cedula_entry.insert(0, values[0])
        self.ui.cedula_entry.config(state="readonly")

        self.ui.nombre_entry.delete(0, tk.END)
        self.ui.nombre_entry.insert(0, values[1])

        self.ui.apellido_entry.delete(0, tk.END)
        self.ui.apellido_entry.insert(0, values[2])

        self.ui.nivel_combobox.set(values[3])

        self.ui.seccion_combobox.set(values[4])

    # AGREGAR o Modificar NOTAS 
    def agregar_notas(self):
        self.ui.messaje["text"] = ""
        try:
            selected_item = self.ui.tree.focus()
            if not selected_item:
                messagebox.showwarning(
                    "Error", "Debe seleccionar un estudiante para agregar notas."
                )
                return

            data = self.ui.tree.item(selected_item)
            if "values" in data:
                cedula_estudiante = data["values"][0]
                nivel_estudiante = data["values"][3]
                seccion_estudiante = data["values"][4]

                VentanaNotas(
                    self.wind,
                    cedula_estudiante=cedula_estudiante,
                    nivel_estudiante=nivel_estudiante,
                    seccion_estudiante=seccion_estudiante,
                    callback_actualizar=self.get_estudiantes,
                )
            else:
                self.ui.messaje.config(fg="#e74c3c")
                self.ui.messaje["text"] = (
                    "Seleccione un estudiante de la tabla para registrar notas."
                )
        except IndexError:
            self.ui.messaje.config(fg="#e74c3c")
            self.ui.messaje["text"] = (
                "Seleccione un estudiante de la tabla para registrar notas."
            )

    # MODIFICAR ESTUDIANTE 
    def modificar_estudiante(self):
        self.ui.messaje["text"] = ""
        try:
            selected_item = self.ui.tree.focus()
            values = self.ui.tree.item(selected_item, "values")

            if not selected_item:
                self.ui.messaje.config(fg="#e74c3c")
                self.ui.messaje["text"] = (
                    "Seleccione un estudiante de la tabla para modificar."
                )
                return

            if values:
                cedula_estudiante = values[0]
                nombre = values[1]
                apellido = values[2]
                nivel = values[3]
                seccion = values[4]

                VentanaModificar(
                    self.wind,
                    cedula_estudiante_orig=cedula_estudiante,
                    nombre_orig=nombre,
                    apellido_orig=apellido,
                    nivel_orig=nivel,
                    seccion_orig=seccion,
                    callback_actualizar=self.get_estudiantes,
                )

        except IndexError:
            self.ui.messaje.config(fg="#e74c3c")
            self.ui.messaje["text"] = (
                "Seleccione un estudiante de la tabla para modificar."
            )
        except Exception as e:
            self.ui.messaje.config(fg="#e74c3c")
            self.ui.messaje["text"] = f"Ocurrió un error inesperado: {e}"

    # ELIMINAR ESTUDIANTE 
    def eliminar_estudiante(self):
        self.ui.messaje["text"] = ""
        try:
            selected_item = self.ui.tree.selection()
            if not selected_item:
                messagebox.showwarning(
                    "Error", "Debe seleccionar un estudiante para eliminar."
                )
                return

            cedula_a_eliminar = self.ui.tree.item(selected_item, "text")

            respuesta = messagebox.askyesno(
                "Confirmar Eliminación",
                f"¿Está seguro de que desea eliminar al estudiante con cédula {cedula_a_eliminar}?",
            )

            if respuesta:
                query = "DELETE FROM estudiantes WHERE cedula_estudiante = ?"
                self.run_query(query, (cedula_a_eliminar,))

                query_notas = "DELETE FROM notas WHERE cedula_estudiante = ?"
                self.run_query(query_notas, (cedula_a_eliminar,))

                self.ui.messaje.config(fg="#2ecc71")
                self.ui.messaje["text"] = (
                    f"Estudiante con cédula {cedula_a_eliminar} eliminado correctamente."
                )
                self.get_estudiantes()
        except Exception as e:
            self.ui.messaje.config(fg="#e74c3c")
            self.ui.messaje["text"] = f"Error al eliminar el estudiante: {e}"

    # DESCARGAR NOTAS A EXCEL 
    def descargar_notas_a_excel(self):
        try:
            selected_item = self.ui.tree.focus()
            if not selected_item:
                messagebox.showwarning(
                    "Error",
                    "Debe seleccionar un estudiante para descargar notas de la sección.",
                )
                return

            values = self.ui.tree.item(selected_item, "values")
            if not values:
                messagebox.showwarning(
                    "Error", "Los datos del estudiante seleccionado no son válidos."
                )
                return

            nivel_seleccionado = values[3]
            seccion_seleccionada = values[4]

            query = """
            SELECT
                e.cedula_estudiante, e.nombre, e.apellido,
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
                messagebox.showinfo(
                    "Información",
                    "No hay datos para descargar para el nivel y sección seleccionados.",
                )
                return

            wb = Workbook()
            ws = wb.active
            ws.title = f"Notas {nivel_seleccionado} {seccion_seleccionada}"

            # 1. Agrega el encabezado
            headers = [
                "N°", 
                "Cédula",
                "Nombre",
                "Apellido",
                "Eval 1",
                "Eval 2",
                "Eval 3",
                "Eval 4",
                "Eval 5",
                "Eval 6",
                "Eval 7",
                "Eval 8",
                "Eval 9",
                "Eval 10",
                "Promedio",
                "TOTAL",
            ]
            ws.append(headers)

            for col in range(1, len(headers) + 1):
                cell = ws.cell(row=1, column=col)
                cell.font = Font(bold=True)
                cell.alignment = Alignment(horizontal="center", vertical="center")

            # 2. Itera sobre los datos y agrega el número de fila
            for i, row in enumerate(data_rows, start=1):
                # Formatea el número de fila a dos dígitos (ej. 1 -> '01')
                row_number_formatted = f"{i:02d}"
                
                # Crea una nueva fila de datos con la numeración al principio
                new_row = [row_number_formatted] + list(row)
                
                # Agrega la nueva fila al Excel
                ws.append(new_row)

            # 3. Ajusta los anchos de las columnas 
            for col in ws.columns:
                max_length = 0
                column = col[0].column_letter
                for cell in col:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except:
                        pass
                adjusted_width = max_length + 2
                ws.column_dimensions[column].width = adjusted_width

            filename = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Archivos de Excel", "*.xlsx")],
                title="Guardar como",
                initialfile=f"Notas_{nivel_seleccionado}_{seccion_seleccionada}.xlsx",
            )

            if filename:
                wb.save(filename)
                messagebox.showinfo(
                    "Éxito",
                    f"Notas guardadas exitosamente en:\n{os.path.basename(filename)}",
                )

        except Exception as e:
            messagebox.showerror(
                "Error", f"Ocurrió un error al descargar el archivo: {e}"
            )

    # BUSCAR POR NIVEL Y SECCIÓN 
    def buscar_nivel_seccion(self):
        """
        Busca y muestra estudiantes por nivel y sección seleccionados.
        """
        nivel_a_buscar = self.ui.nivel_search_combobox.get()
        seccion_a_buscar = self.ui.seccion_search_combobox.get()

        if not nivel_a_buscar or not seccion_a_buscar:
            self.ui.messaje.config(
                text="❌ Por favor, seleccione un nivel y una sección para buscar.", fg="#e74c3c"
            )
            return

        # Limpiar el Treeview y el mensaje de estado
        records = self.ui.tree.get_children()
        for element in records:
            self.ui.tree.delete(element)
        self.ui.messaje.config(text="")

        query = "SELECT cedula_estudiante, nombre, apellido, nivel, seccion FROM estudiantes WHERE nivel = ? AND seccion = ? ORDER BY CAST(cedula_estudiante AS INTEGER) ASC;"
        parameters = (nivel_a_buscar, seccion_a_buscar)
        db_rows = self.run_query(query, parameters)

        found = False
        for row in db_rows:
            self.ui.tree.insert("", "end", text=row[0], values=row[0:])
            found = True

        if found:
            self.ui.messaje.config(
                text=f"✅ Estudiantes del nivel {nivel_a_buscar} sección {seccion_a_buscar} mostrados.",
                fg="#2ecc71",
            )
        else:
            self.ui.messaje.config(
                text=f"❌ No se encontraron estudiantes para el nivel {nivel_a_buscar} sección {seccion_a_buscar}.",
                fg="#e74c3c",
            )
    #Busqueda de estudiantes por numero de cedula
    def buscar_estudiante_por_cedula(self):
        """
        Busca un estudiante por su cédula en la BD y actualiza el Treeview
        para mostrar solo el resultado encontrado.
        """
        cedula_a_buscar = self.ui.search_entry.get().strip()
        
        if not cedula_a_buscar:
            self.ui.messaje.config(
                text="Por favor, ingrese una cédula para buscar.", fg="#e74c3c"
            )
            return

        # Limpiar el Treeview y el mensaje de estado antes de la búsqueda
        records = self.ui.tree.get_children()
        for element in records:
            self.ui.tree.delete(element)
        self.ui.messaje.config(text="")
        
        # Consulta SQL para buscar por cédula
        query = "SELECT cedula_estudiante, nombre, apellido, nivel, seccion FROM estudiantes WHERE cedula_estudiante = ?;"
        parameters = (cedula_a_buscar,)
        
        # Ejecutar la consulta y obtener el primer resultado
        db_row = self.run_query(query, parameters).fetchone()

        # Limpiar el campo de búsqueda al finalizar
        self.ui.search_entry.delete(0, tk.END)

        if db_row:
            # Si se encuentra, inserta SOLO ese estudiante en el Treeview
            self.ui.tree.insert("", "end", text=db_row[0], values=db_row[0:])
            
            # Resaltar (seleccionar y enfocar) el único elemento en el Treeview
            iid = self.ui.tree.get_children()[0] 
            self.ui.tree.selection_set(iid)
            self.ui.tree.focus(iid)
            
            self.ui.messaje.config(
                text=f"✅ Estudiante encontrado: {db_row[1]} {db_row[2]}", 
                fg="#2ecc71"
            )
        else:
            self.ui.messaje.config(
                text=f"❌ No se encontró un estudiante con la cédula: {cedula_a_buscar}",
                fg="#e74c3c",
            )
   
   #Borrar todos los estudiantes
    def borrar_todas_las_notas(self):
        respuesta = messagebox.askyesno(
            "Confirmar",
            "¿Está seguro de que desea borrar todas las notas de todos los estudiantes? Esta acción es irreversible.",
        )
        if respuesta:
            query = "DELETE FROM notas"
            self.run_query(query)
            messagebox.showinfo(
                "Éxito", "Todas las notas han sido borradas correctamente."
            )
            self.get_estudiantes()

    def borrar_todo(self):

        respuesta = messagebox.askyesno(
            "Confirmar",
            "ADVERTENCIA: ¿Está seguro de que desea borrar TODOS los estudiantes y TODAS sus notas? Esta acción es irreversible.",
        )
        if respuesta:
            query_estudiantes = "DELETE FROM estudiantes"
            self.run_query(query_estudiantes)
            query_notas = "DELETE FROM notas"
            self.run_query(query_notas)
            messagebox.showinfo(
                "Éxito",
                "Todos los estudiantes y sus notas han sido borrados correctamente.",
            )
            self.get_estudiantes()


if __name__ == "__main__":
    window = tk.Tk()
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
# AppAcademi/dist/index2 AppAcademi/dist/registro_estudiante.db


# para cargar carpeta        pyinstaller --windowed index2.py


#  ejecutable         pyinstaller --onefile --noconsole index2.py

#   /home/aquiles/Documentos/MiAcademi/AppAcademi/venv/bin/python
