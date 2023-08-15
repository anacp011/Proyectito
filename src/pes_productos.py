import tkinter as tk
from tkinter import ttk
import pymysql
from producto_dialog import ProductoDialog
from consultas_sql import ConexionDB
from tkinter import messagebox

class ProductoApp:
    def __init__(self, parent, cuaderno1):
        self.parent = parent
        self.cuaderno1 = cuaderno1
        pestana_productos = tk.Frame(self.cuaderno1)
        self.cuaderno1.add(pestana_productos, text="Productos")

        #Contenedores
        frame1 = tk.LabelFrame(pestana_productos, text="Consulta de Productos", font=("calibri", 10), relief=tk.SUNKEN)
        frame1.pack(fill="both", expand="yes", padx=20, pady=3)
        
        frame2 = tk.LabelFrame(pestana_productos, text="Informacion de Productos", font=("calibri", 10), relief=tk.SUNKEN)
        frame2.pack(fill="both", expand="yes", padx=20, pady=20)
        
        #Variables
        self.ID = tk.StringVar()
        self.Nombre = tk.StringVar()
        self.Cantidad = tk.StringVar()
        self.Fecha_vencimiento = tk.StringVar()
        
        # Tabla
        self.trv = ttk.Treeview(frame2, columns=(1, 2, 3, 4), show="headings", height="10")
        self.trv.pack()
        self.trv.heading(1, text="ID ")
        self.trv.heading(2, text="Nombre")
        self.trv.heading(3, text="Cantidad")
        self.trv.heading(4, text="Fecha_vencimiento")
        self.trv.bind("<Double-Button-1>", self.editar_datos)
        
        # Elementos
        lbl = tk.Label(frame1, text="Consulta")
        lbl.pack(side=tk.LEFT)
        self.q = tk.StringVar()
        ent = tk.Entry(frame1, textvariable=self.q)
        ent.pack(side=tk.LEFT)
        
        #Botones
        btn = tk.Button(frame1, text="Buscar", command=self.consulta)
        btn.pack(side=tk.LEFT, padx=6)
        btn = tk.Button(frame1, text="Restablecer", command=self.restablecer)
        btn.pack(side=tk.LEFT, padx=6)
        
        btn = tk.Button(frame2, text="Agregar", command=self.abrir_ventana_agregar_editar)
        btn.pack(side=tk.LEFT, padx=300)
        btn = tk.Button(frame2, text="Eliminar", command=self.eliminar)
        btn.pack(side=tk.LEFT)
        
        self.actualizar()
        
    def editar_datos(self, event):
        item = self.trv.focus()
        ProductoDialog(self, item)

    def abrir_ventana_agregar_editar(self):
        ProductoDialog(self)
        
    def vista(self, rows):
        self.trv.delete(*self.trv.get_children())
        for i in rows:
            self.trv.insert("", "end", values=i)
    
    def actualizar(self):
        try:
            conexion = ConexionDB(self)  # Crea una instancia de la clase ConexionDB
            conexion.actualizar_producto()
        except pymysql.Error as e:
            messagebox.showerror("Error", f"No se pudo actualizar la tabla de productos: {str(e)}")
        finally:
            conexion.close()
            
    def consulta(self):
        q2 = self.q.get()
        try:
            conexion = ConexionDB(self)  # Crea una instancia de la clase ConexionDB
            conexion.consulta_producto(q2)
        except pymysql.Error as e:
            messagebox.showerror("Error", f"No se pudo realizar la consulta de productos: {str(e)}")
        finally:
            conexion.close()
            
    def restablecer(self):
        self.q.set("")
        self.actualizar()
    
    def eliminar(self):
        selected_item = self.trv.focus()
        if selected_item:
            values = self.trv.item(selected_item)["values"]
            
            confirmation = messagebox.askyesno("Eliminar producto", "¿Está seguro que desea eliminar este producto?")
            if confirmation:
                try:
                    conexion = ConexionDB(self)  
                    conexion.eliminar_producto(values)  
                    conexion.close() 
                    self.actualizar()
                except pymysql.Error as e:
                    messagebox.showerror("Error", f"No se pudo eliminar el producto: {str(e)}")
        else:
            messagebox.showerror("Eliminar producto", "No ha seleccionado ningun producto")
    


