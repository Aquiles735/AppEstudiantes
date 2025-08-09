
import tkinter as tk
from tkinter import ttk
from tkinter.ttk import Label, LabelFrame 

class Widgets:
    def __init__(self, parent, controller):
        self.parent = parent
        self.controller = controller

        main_container = tk.Frame(self.parent, bg='#2c3e50')
        main_container.pack(fill='both', expand=True, padx=10, pady=10)
        
        frame = LabelFrame(main_container, text='Registro de Estudiantes', style='My.TLabelframe')
        frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        main_container.grid_columnconfigure(0, weight=1)
        main_container.grid_columnconfigure(1, weight=2)
        frame.grid_columnconfigure(0, weight=0)
        frame.grid_columnconfigure(1, weight=0)
        frame.grid_columnconfigure(2, weight=0)
        frame.grid_columnconfigure(3, weight=0)

        Label(frame, text='Cédula').grid(row=0, column=0, padx=2, pady=5, sticky='e')
        self.cedula_entry = ttk.Entry(frame)
        self.cedula_entry.grid(row=0, column=1, padx=2, pady=5, sticky='ew')

        Label(frame, text='Nombre:').grid(row=0, column=2, padx=2, pady=5, sticky='e')
        self.nombre_entry = ttk.Entry(frame)
        self.nombre_entry.grid(row=0, column=3, padx=2, pady=5, sticky='ew')

        Label(frame, text='Apellido:').grid(row=1, column=0, padx=2, pady=5, sticky='e')
        self.apellido_entry = ttk.Entry(frame)
        self.apellido_entry.grid(row=1, column=1, padx=2, pady=5, sticky='ew')

        Label(frame, text='Nivel:').grid(row=1, column=2, padx=2, pady=5, sticky='e')
        opciones_nivel = ['1 año', '2 año', '3 año', '4 año', '5 año', '6 año']
        self.nivel_combobox = ttk.Combobox(frame, values=opciones_nivel)
        self.nivel_combobox.set(opciones_nivel[0])
        self.nivel_combobox.grid(row=1, column=3, padx=2, pady=5, sticky="ew")

        Label(frame, text='Sección:').grid(row=2, column=0, padx=2, pady=5, sticky='e')
        opciones_seccion = ['A','B','C','D','E','F','G','H']
        self.seccion_combobox = ttk.Combobox(frame, values=opciones_seccion)
        self.seccion_combobox.set(opciones_seccion[0])
        self.seccion_combobox.grid(row=2, column=1, padx=2, pady=5, sticky="ew")


        # Botones
        btn_registrar = ttk.Button(frame, text='Registrar Estudiante', command=controller.resgist_estud)
        btn_registrar.grid(row=3, column=0, columnspan=4, sticky='we', padx=100, pady=10)
        btn_registrar.bind('<Return>', lambda event: btn_registrar.invoke())
        Label(frame, text='Seleccionar un estudiante para registrar o modificar nota').grid(row=4, column=0,columnspan=4, sticky='we', padx=180, pady=(10,0))
        
        btn_notas = ttk.Button(frame, text='Registrar Notas', command=controller.agregar_notas)
        btn_notas.grid(row=5, column=0, columnspan=4, sticky='we', padx=150, pady= 10)
        btn_notas.bind('<Return>', lambda event: btn_notas.invoke())
        Label(frame, text='Seleccionar un estudiante para modificar Datos (No modifica la Cédula)').grid(row=6, column=0, columnspan=4, sticky='we', padx=140, pady=(10,0))
        
        btn_modificar = ttk.Button(frame, text='Modificar datos de Estudiante', command=controller.modificar_estudiante)
        btn_modificar.grid(row=7, column=0, columnspan=4, sticky='we', padx=150, pady=10)
        btn_modificar.bind('<Return>', lambda event: btn_modificar.invoke())
        Label(frame, text='Seleccionar un estudiante para retirarlo del registro').grid(row=8, column=0,columnspan=4, sticky='we', padx=190, pady=(10,0))
        
        btn_eliminar = ttk.Button(frame, text='Eliminar Estudiante', command=controller.eliminar_estudiante)
        btn_eliminar.grid(row=9, column=0, columnspan=4, sticky='we', padx=150, pady=10)
        btn_eliminar.bind('<Return>', lambda event: btn_eliminar.invoke())
        Label(frame, text='Seleccionar un estudiante para descargar en EXCEL las notas de la sección ').grid(row=10, column=0, columnspan=4, sticky='we', padx=120, pady=(10,0))
        
        btn_descargar = ttk.Button(frame, text='Descargar Notas en EXCEL', command=controller.descargar_notas_a_excel)
        btn_descargar.grid(row=12, column=0, columnspan=4, sticky='we', padx=150, pady=(10,0))
        btn_descargar.bind('<Return>', lambda event: btn_descargar.invoke())
        
        btn_salir = ttk.Button(frame, text='Salir', command=self.parent.destroy)
        btn_salir.grid(row=14, column=0, columnspan=4, sticky='we', padx=200, pady=10)
        btn_salir.bind('<Return>', lambda event: btn_salir.invoke())
        
        self.messaje = tk.Label(frame, text='', bg='#34495e', fg='#e74c3c', font=('Helvetica', 10, 'bold')) 
        self.messaje.grid(row=13, column=0, columnspan=4, sticky='we')

        self.tree = ttk.Treeview(main_container, columns=('col0', 'col1', 'col2', 'col3','col4'), show='headings')
        self.tree.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        scrollbar = ttk.Scrollbar(main_container, orient="vertical", command=self.tree.yview)
        scrollbar.grid(row=0, column=2, sticky='ns')
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        main_container.grid_rowconfigure(0, weight=1)
        self.tree.heading('col0', text='Cédula', anchor=tk.CENTER)
        self.tree.heading('col1', text='Nombre', anchor=tk.CENTER)
        self.tree.heading('col2', text='Apellido', anchor=tk.CENTER)
        self.tree.heading('col3', text='Nivel', anchor=tk.CENTER)
        self.tree.heading('col4', text='Secc', anchor=tk.CENTER)
      
        self.tree.column('col0', width=90)
        self.tree.column('col1', width=90)
        self.tree.column('col2', width=90)
        self.tree.column('col3', width=50)
        self.tree.column('col4', width=50)


        #Botones para borrar notas  o todo
        botones_frame = tk.Frame(self.parent, bg='#2c3e50')
        botones_frame.pack(side='bottom', fill='x', padx=10, pady=10)
        
        self.borrar_todo_btn = ttk.Button(botones_frame, text="Borrar todos los estudiantes y notas", style='Red.TButton', command=controller.borrar_todo, takefocus=0)
        self.borrar_todo_btn.pack(side='right', padx=5)

        self.borrar_notas_btn = ttk.Button(botones_frame, text="Borrar todas las notas", style='Red.TButton', command=controller.borrar_todas_las_notas, takefocus=0)
        self.borrar_notas_btn.pack(side='right', padx=5)
        