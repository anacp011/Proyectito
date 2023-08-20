import tkinter as tk
from tkinter import ttk
import pymysql
from compra_dialog import CompraDialog
from consultas_sql import ConexionDB
from tkinter import messagebox

class CompraApp:
    def __init__(self, parent, cuaderno1):
        self.parent = parent
        self.cuaderno1 = cuaderno1
        pestana_compra = tk.Frame(self.cuaderno1)
        self.cuaderno1.add(pestana_compra, text="Compra")

        #Contenedores
        frame1 = tk.LabelFrame(pestana_compra, text="Consulta de compra", font=("calibri", 10), relief=tk.SUNKEN)
        frame1.pack(fill="both", expand="yes", padx=20, pady=3)
        
        frame2 = tk.LabelFrame(pestana_compra, text="Informacion de compra", font=("calibri", 10), relief=tk.SUNKEN)
        frame2.pack(fill="both", expand="yes", padx=20, pady=20)
        
        #Variables
        self.ID = tk.StringVar()
        self.ID_cliente = tk.StringVar()
        self.ID_producto = tk.StringVar()
        self.Cantidad = tk.StringVar()
        self.Fecha_compra = tk.StringVar()
        
        # Tabla
        self.trv = ttk.Treeview(frame2, columns=(1, 2, 3, 4, 5), show="headings", height="10")
        self.trv.pack()
        self.trv.heading(1, text="ID ")
        self.trv.heading(2, text="ID Cliente")
        self.trv.heading(3, text="ID Producto")
        self.trv.heading(4, text="Fecha_compra")
        self.trv.heading(5, text="Cantidad")
        
        
        self.trv.bind("<Double-Button-1>", self.editar_datos)
        
        # Elementos
        lbl = tk.Label(frame1, text="Consulta")
        lbl.pack(side=tk.LEFT)
        self.q = tk.StringVar()
        ent = tk.Entry(frame1, textvariable=self.q)
        ent.pack(side=tk.LEFT)
        
        #Botones
        btn = tk.Button(frame1, text="Buscar")
        btn.pack(side=tk.LEFT, padx=6)
        btn = tk.Button(frame1, text="Restablecer")
        btn.pack(side=tk.LEFT, padx=6)
        btn = tk.Button(frame2, text="Agregar", command=self.abrir_ventana_agregar_editar)
        btn.pack(side=tk.LEFT, padx=300)
        btn = tk.Button(frame2, text="Eliminar", command=self.eliminar)
        btn.pack(side=tk.LEFT)
        
        self.actualizar()
    
    def editar_datos(self, event):
        item = self.trv.focus()
        CompraDialog(self, item)
        
    def abrir_ventana_agregar_editar(self):
        CompraDialog(self)
    
    def vista(self, rows):
        self.trv.delete(*self.trv.get_children())
        for i in rows:
            self.trv.insert("", "end", values=i)
    
    def actualizar(self):
        try:
            conexion = ConexionDB(self)  # Crea una instancia de la clase ConexionDB
            conexion.actualizar_compra()
        except pymysql.Error as e:
            messagebox.showerror("Error", f"No se pudo actualizar la tabla de compra: {str(e)}")
        finally:
            conexion.close()
    
            
    def restablecer(self):
        self.q.set("")
        self.actualizar()
    
    def eliminar(self):
        selected_item = self.trv.focus()
        if selected_item:
            values = self.trv.item(selected_item)["values"]
            
            confirmation = messagebox.askyesno("Eliminar compra", "¿Está seguro que desea eliminar este compra?")
            if confirmation:
                try:
                    conexion = ConexionDB(self)  
                    conexion.eliminar_compra(values)  
                    conexion.close() 
                    self.actualizar()
                except pymysql.Error as e:
                    messagebox.showerror("Error", f"No se pudo eliminar el compra: {str(e)}")
        else:
            messagebox.showerror("Eliminar compra", "No ha seleccionado ningun compra")
    


