
import tkinter as tk
from tkinter import ttk

class Diseno:
   
    def __init__(self, window):
       
        self.wind = window
        self.style = ttk.Style()
        self.style.theme_use('clam')  # Un tema base que es fácil de modificar

        # Estilo para el LabelFrame
        self.style.configure(
            'My.TLabelframe',
            background='#34495e',
            bordercolor='#2c3e50',
            borderwidth=5
        )
        self.style.configure(
            'My.TLabelframe.Label',
            background='#34495e',
            foreground='white',
            font=('Helvetica', 12, 'bold')
        )
        
        # Estilo para las etiquetas de los campos de entrada
        self.style.configure(
            'TLabel',
            background='#34495e',
            foreground='#ecf0f1',
            font=('Helvetica', 10)
        )
        
        # Estilo para las etiquetas de los mensajes 
        self.style.configure(
            'Highlight.TLabel',
            background='#34495e',
            foreground='#7de918',
            font=('Helvetica', 10)
        )

        # Estilo para los botones
        self.style.configure(
            'TButton',
            background='#3498db',  # Azul original
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
        
        # Estilo para los botones rojos
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
            background=[('selected', '#3498db')]  # Resalta la fila seleccionada
        )