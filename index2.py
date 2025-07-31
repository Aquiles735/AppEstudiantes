from itertools import product
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
       # frame = LabelFrame(self.wind, text='Registro y control')
        #frame.grid(row=0, column=0, columnspan=3, pady=20)
        self.wind.title('Inicio Registro')
        #contenedor inicial
        frame = LabelFrame(self.wind, text='Control Institucional')
        frame.grid(row=1, column=0, columnspan=3, pady=20)
    
        ttk.Button(text='Registrar Est.', command=self.agregar_estudiante).grid(row=2, column=0,sticky=W + E )
        frame.grid(row=2, column=4, columnspan=3, pady=20)
        ttk.Button(text='Registrar Prof.').grid(row=2, column=2,sticky=W + E )

##-----------------------##
    def agregar_estudiante(self):
        
        #self.wind.title('Institucional')
        self.agregar_estudiante= Toplevel()
        self.agregar_estudiante.title = 'Agregar estudiante'
   
        #contenedor estudiante
        frame = LabelFrame(self.wind, text='Control estudiantes')
        frame.grid(row=2, column=4, columnspan=3, pady=20)

        # input de datos 'Nivel de estudio' 
        Label(frame, text= 'Nivel:').grid(row=0, column=0)
        self.nivel=Entry(frame)
        #para que el cursor este en el campo al iniciar
        self.nivel.focus()
        self.nivel.grid(row=0, column=1)

        # Seccion de estudio
        Label(frame, text= 'Seccion:').grid(row=0, column=2)
        self.seccion=Entry(frame)
        self.seccion.grid(row=0, column=3)

        Label(frame, text= 'Nombre:').grid(row=1, column=0)
        self.nombre=Entry(frame)
        self.nombre.grid(row=1, column=1)

        Label(frame, text= 'Apellido:').grid(row=1, column=2)
        self.apellido=Entry(frame)
        self.apellido.grid(row=1, column=3)      

        ttk.Button(frame, text='Registrar Estudiante').grid(row=2,column=1, columnspan= 3, sticky= W+E)
    """  
        #panel profesor
        self.wind.title('Institucional')
        self.agregar_profesor= Toplevel()
        self.agregar_profesor.title = 'Agregar profesor'
        #contenedor profesor
        frame = LabelFrame(self.wind, text='Control profesores')
        frame.grid(row=7, column=4, columnspan=3, pady=20)

        # input de datos 'name' 
        Label(frame, text= 'Nombre:').grid(row=3, column=0)
        self.nombre=Entry(frame)
        #para que el cursor este en el campo al iniciar
        self.nombre.focus()
        self.nombre.grid(row=3, column=1)

        #otro input
        Label(frame, text= 'Apellido:').grid(row=3, column=2)
        self.apellido=Entry(frame)
        self.apellido.grid(row=3, column=3)

        Label(frame, text= 'Email:').grid(row=5, column=0)
        self.email=Entry(frame)
        self.email.grid(row=5, column=1)

        Label(frame, text= 'Area:').grid(row=5, column=2)
        self.area=Entry(frame)
        self.area.grid(row=5, column=3)      

        ttk.Button(frame, text='Registrar Profesor').grid(row=7,column=1, columnspan= 3, sticky= W+E)

"""

 

if __name__== '__main__':
    window = Tk()
    apliclation = Control(window)
    window.mainloop()

# en PythonCrud iniciar aplicación 
# python3 index2.py
# para git, github abrir AppPythonCrud
