
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
        ttk.Button(text='Registrar Prof.', command=self.agrgar_profesor).grid(row=4, column=1, columnspan=1,sticky=W + E )
        self.tree=ttk.Treeview(height= 20, columns=3)
        self.tree.grid(row=5, column=0, columnspan=3)
        self.tree.heading('#0', text='Nombre', anchor= CENTER)
        self.tree.heading('#1', text='Apellido', anchor= CENTER)
        

      #panel profesor
        
    def agrgar_profesor(self):
       
        self.agrgar_profesor=Toplevel()
        #self.agrgar_profesor.title='Agragar Profesor'
       
        Label(self.agrgar_profesor,text= 'Nombre:').grid(row=0, column=0,pady=20,padx=10)
        self.nivel=Entry(self.agrgar_profesor)
        #para que el cursor este en el campo al iniciar
        self.nivel.focus()
        self.nivel.grid(row=0, column=1)

        # Seccion de estudio
        Label(self.agrgar_profesor,text= 'Apellido:').grid(row=0, column=2,pady=20,padx=10)
        self.seccion=Entry(self.agrgar_profesor)
        self.seccion.grid(row=0, column=3,padx=20)

        Label(self.agrgar_profesor,text= 'Email:').grid(row=1, column=0)
        self.nombre=Entry(self.agrgar_profesor)
        self.nombre.grid(row=1, column=1)
    
        ttk.Button(self.agrgar_profesor,text='Registrar Profesor').grid(row=2,column=0,columnspan=4, sticky= W+E,pady=20,padx=30)

        self.tree=ttk.Treeview(self.agrgar_profesor,height= 20,columns=3)
        self.tree.grid(row=5, column=0, columnspan=3)
        self.tree.heading('#0', text='Nombre', anchor= CENTER)
        self.tree.heading('#1', text='Apellido',anchor=CENTER)
       
       
      
      

 

if __name__== '__main__':
        window = Tk()
        apliclation = Control(window)
        window.mainloop()

# en PythonCrud iniciar aplicación 
# python3 index2.py
# para git, github abrir AppPythonCrud
