import tkinter as tk
from tkinter import ttk
import pymysql
from tkinter import messagebox


class ProductoApp:
    def __init__(self,cuaderno1):
        
        self.cuaderno1 = cuaderno1
        pestana_productos = tk.Frame(self.cuaderno1)
        self.cuaderno1.add(pestana_productos, text="Productos")

        #Contenedores
        frame1 = tk.LabelFrame(pestana_productos, text="Consulta de Productos", font=("calibri", 10), relief=tk.SUNKEN)
        frame1.pack(fill="both", expand="yes", padx=20, pady=3)
        
        frame2 = tk.LabelFrame(pestana_productos, text="Informacion de Productos", font=("calibri", 10), relief=tk.SUNKEN)
        frame2.pack(fill="both", expand="yes", padx=20, pady=3)
        
        #Variables
        self.ID = tk.StringVar()
        self.Nombre = tk.StringVar()
        self.Fecha_vencimiento = tk.StringVar()
        self.Cantidad = tk.StringVar()
        
        # Tabla
        self.trv = ttk.Treeview(frame2, columns=(1, 2, 3, 4), show="headings", height="8")
        self.trv.pack()
        self.trv.heading(1, text="ID ")
        self.trv.heading(2, text="Nombre")
        self.trv.heading(3, text="Fecha_vencimiento")
        self.trv.heading(4, text="Cantidad")
        
        # Elementos
        lbl = tk.Label(frame1, text="Consulta")
        lbl.pack(side=tk.LEFT)
        self.q = tk.StringVar()
        ent = tk.Entry(frame1, textvariable=self.q)
        ent.pack(side=tk.LEFT)
        
        #Botones
        btn = tk.Button(frame1, text="Buscar", command=self.consulta)
        btn.pack()
        btn = tk.Button(frame1, text="Restablecer", command=self.restablecer) 
        btn.pack()
        btn = tk.Button(frame1, text="Guardar", command=self.agregar_editar_datos) 
        btn.pack()
        
        #Conexión bbdd
        schemacs = pymysql.connect(host="localhost", user="root", password="123456", database="schemacs")
        cursor = schemacs.cursor()
        query = "SELECT ID, Nombre, Fecha_vencimiento, Cantidad FROM producto"
        cursor.execute(query)
        rows = cursor.fetchall()
        self.vista(rows)
        schemacs.close()
        
    #Funciones    
    def vista(self, rows):
        self.trv.delete(*self.trv.get_children())
        for i in rows:
            self.trv.insert('', 'end', values=i)
            
    def restablecer(self):
        schemacs = pymysql.connect(host="localhost", user="root", password="123456", database="schemacs")
        cursor = schemacs.cursor()
        query = "SELECT ID, Nombre, Fecha_vencimiento, Cantidad FROM producto"
        cursor.execute(query)
        rows = cursor.fetchall()
        self.vista(rows)
        schemacs.close()

    def consulta(self):
        q2 = self.q.get()
        schemacs = pymysql.connect(host="localhost", user="root", password="123456", database="schemacs")
        cursor = schemacs.cursor()
        query = "SELECT ID, Nombre, Fecha_vencimiento, Cantidad FROM producto WHERE Nombre LIKE '%" + q2 + "%' OR Cantidad LIKE '%" + q2 + "%' OR ID LIKE '%" + q2 + "%' "
        cursor.execute(query)
        rows = cursor.fetchall()
        self.vista(rows)
        schemacs.close()
        
    def agregar_editar_datos(self):
        if self.ID.get() == "" or self.Nombre.get() == "" or self.Fecha_vencimiento.get() == "":
            messagebox.showerror("Control de Stock", "Ingrese información en todos los campos")
        else:
            schemacs = pymysql.connect(host="localhost", user="root", password="123456", database="schemacs")
            cursor = schemacs.cursor()
            cursor.execute("UPDATE producto SET ID=%s, Nombre=%s, Fecha_vencimiento=%s, Cantidad=%s WHERE ID=%s", (
                self.ID.get(),
                self.Nombre.get(),
                self.Fecha_vencimiento.get(),
                self.Cantidad.get(),
            ))
            schemacs.commit()
            schemacs.close()
            messagebox.showinfo("Datos Completados", "Se agregaron correctamente")
            self.ID.set("")
            self.Nombre.set("")
            self.Fecha_vencimiento.set("")
            self.Cantidad.set("")
        
        


