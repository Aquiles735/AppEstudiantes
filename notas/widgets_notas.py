
import tkinter as tk
from tkinter import ttk

def create_widgets(self, master, cedula_estudiante=None):
    self.title("Registrar Notas")
    self.transient(master)  
    self.grab_set()
    self.resizable(False, False)
    self.config(bg='#34495e')
    
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
    self.messaje = tk.Label(contenedor_widgets, text='', bg='#34495e', fg='#e74c3c', font=('Helvetica', 10, 'bold'))
    self.messaje.grid(row=6, column=0, columnspan=2, sticky='ew', pady=5)

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

    ttk.Label(contenedor_widgets, text='N° Evaluaciones del LAPSO:').grid(row=3, column=0, pady=5, padx=5, sticky="e")
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
    
    btn_salir = ttk.Button(contenedor_widgets, text='Salir', command=self.salir_con_advertencia, style='Accent.TButton')
    btn_salir.grid(row=5, column=1, pady=5, padx=5, sticky="we")
    btn_salir.bind('<Return>', lambda event=None: self.salir_con_advertencia())

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
    self.tree.heading('col5', text='Eval 5', anchor='center')
    self.tree.heading('col6', text='Eval 6', anchor='center')
    self.tree.heading('col7', text='Eval 7', anchor='center')
    self.tree.heading('col8', text='Eval 8', anchor='center')
    self.tree.heading('col9', text='Eval 9', anchor='center')
    self.tree.heading('col10', text='Eval 10', anchor='center')
    self.tree.heading('col11', text='Promedio', anchor='center')
    self.tree.heading('col12', text='TOTAL', anchor='center')
    self.tree.heading('col13', text='Nota Definitiva', anchor='center')

    self.tree.column('col1', width=100)
    self.tree.column('col2', width=60)
    self.tree.column('col3', width=60)
    self.tree.column('col4', width=60)
    self.tree.column('col5', width=60)
    self.tree.column('col6', width=60)
    self.tree.column('col7', width=60)
    self.tree.column('col8', width=60)
    self.tree.column('col9', width=60)
    self.tree.column('col10', width=60)
    self.tree.column('col11', width=80)
    self.tree.column('col12', width=80)
    self.tree.column('col13', width=100)

    self.get_notes()  
    
    self.update_idletasks()
    width = self.winfo_width()
    height = self.winfo_height()
    x = (self.winfo_screenwidth() // 2) - (width // 2)
    y = (self.winfo_screenheight() // 2) - (height // 2)
    self.geometry(f'{width}x{height}+{x}+{y}')