import tkinter as tk
from tkinter import ttk
from tkinter import *
import sqlite3



                         #python3 -m venv venv
                         #source venv/bin/activate
class Control:
    #nombre base de datos , para conectar la y  a creada BD
    db_name = 'Institucional.db'

    def __init__ (self,window):
        self.wind=window
        
        #contenedor inicial
        self.wind.title('Inicio Registro')
        #contenedor inicial
        frame = LabelFrame(self.wind, text='Registro Estudiante')
        frame.grid(row=0, column=0, columnspan=3, pady=20,padx=100)
       
       

       #Agregar estudiante 
  
        #contenedor estudiante
        # input de datos 'Nivel de estudio' 
        Label( frame,text= 'Nivel:').grid(row=0, column=0)
        self.nivel=Entry(frame)
        #para que el cursor este en el campo al iniciar
        self.nivel.focus()
        self.nivel.grid(row=0, column=1)

        # Seccion de estudio
        Label(frame, text= 'Seccion:').grid(row=0, column=2)
        self.seccion=Entry(frame)
        self.seccion.grid(row=0, column=3)

        Label(frame,text= 'Nombre:').grid(row=1, column=0)
        self.nombre=Entry(frame)
        self.nombre.grid(row=1, column=1)

        Label( frame,text= 'Apellido:').grid(row=1, column=2)
        self.apellido=Entry(frame)
        self.apellido.grid(row=1, column=3)      

        ttk.Button(frame, text='Registrar Estudiante').grid(row=2,column=1, columnspan= 3, sticky= W+E)
        ttk.Button(text='Registrar Prof.', command=self.agregar_profesor).grid(row=4, column=0, columnspan=1,sticky=W + E )
        self.tree=ttk.Treeview(columns=('col0', 'col1', 'col2', 'col3'), show='headings')
        self.tree.grid(row=5, column=0)
        self.tree.heading('col0', text='Nivel', anchor= CENTER)
        self.tree.heading('col1', text='Seccion', anchor= CENTER)
        self.tree.heading('col2', text='Nombre', anchor= CENTER)
        self.tree.heading('col3', text='Apellido', anchor= CENTER)
        

      #panel profesor
        
    def agregar_profesor(self):                       
        
        self.agregar_profesor=Toplevel()
        #self.agregar_profesor.title='Agragar Profesor'
       
        Label(self.agregar_profesor,text= 'Nombre:').grid(row=0, column=0)
        self.nivel=Entry(self.agregar_profesor)
        #para que el cursor este en el campo al iniciar
        self.nivel.focus()
        self.nivel.grid(row=0, column=1)

        # Seccion de estudio
        Label(self.agregar_profesor,text= 'Apellido:').grid(row=0, column=2)
        self.seccion=Entry(self.agregar_profesor)
        self.seccion.grid(row=0, column=3)

        Label(self.agregar_profesor,text= 'Email:').grid(row=1, column=0)
        self.nombre=Entry(self.agregar_profesor)
        self.nombre.grid(row=1, column=1)
    
        ttk.Button(self.agregar_profesor,text='Registrar Profesor').grid(row=2,column=0, sticky= W+E)

        self.tree=ttk.Treeview(self.agregar_profesor,columns=('col0', 'col1', 'col2'),show= 'headings')
        self.tree.grid(row=5, column=0)
        self.tree.heading('col0', text='Nombre', anchor= CENTER)
        self.tree.heading('col1', text='Apellido',anchor=CENTER)
        self.tree.heading('col2', text='Email',anchor=CENTER)
        
       
       
      
      

 

if __name__== '__main__':
        window = Tk()
        apliclation = Control(window)
        window.mainloop()

# en PythonCrud iniciar aplicación 
# python3 index2.py
# para git, github abrir AppPythonCrud
