import tkinter as tk
from tkinter import messagebox
from tkcalendar import *
from tkcalendar import DateEntry
from datetime import datetime
import pymysql

class CompraDialog:
    def __init__(self, parent, parent_compra, item=None, callback=None):
        self.parent = parent
        self.parent_compra = parent_compra
        self.callback = callback
        self.dialog = tk.Toplevel(self.parent.parent)
        self.dialog.title("Agregar/Editar Compra")
        self.dialog.geometry("380x350")

        frame = tk.Frame(self.dialog)
        frame.pack(pady=60)

        tk.Label(frame, text="ID compra:").grid(row=0, column=0, sticky="e")
        self.ID = tk.Entry(frame)
        self.ID.grid(row=0, column=1)
        
        tk.Label(frame, text="ID Cliente:").grid(row=1, column=0, sticky="e")
        self.ID_cliente = tk.Entry(frame)
        self.ID_cliente.grid(row=1, column=1)
        
        tk.Label(frame, text="ID Producto:").grid(row=2, column=0, sticky="e")
        self.ID_producto = tk.Entry(frame)
        self.ID_producto.grid(row=2, column=1)
        
        tk.Label(frame, text="Cantidad:").grid(row=3, column=0, sticky="e")
        self.Cantidad = tk.Entry(frame)
        self.Cantidad.grid(row=3, column=1)

        tk.Label(frame, text="Fecha compra:").grid(row=4, column=0, sticky="e")
        
        if item:
            self.Fecha_compra = DateEntry(frame)
        else:
            self.Fecha_compra = DateEntry(frame, date_pattern='yyyy/mm/dd')
        
        self.Fecha_compra.grid(row=4, column=1)
        
        btn_frame = tk.Frame(self.dialog)
        btn_frame.pack(pady=10)

        if item:
            values = self.parent_compra.trv.item(item, 'values')
            self.ID.insert(tk.END, values[0])
            self.ID_cliente.insert(tk.END, values[1])
            self.ID_producto.insert(tk.END, values[2])
            self.Cantidad.insert(tk.END, values[3])
            self.Fecha_compra.delete(0, tk.END)
            self.Fecha_compra.insert(tk.END, values[4])
            

            tk.Button(btn_frame, text="Actualizar", command=self.modificar_datos).pack(side=tk.LEFT, padx=10)
        else:
            tk.Button(btn_frame, text="Agregar", command=self.guardar_datos).pack(side=tk.LEFT, padx=10)

        tk.Button(btn_frame, text="Cancelar", command=self.dialog.destroy).pack(side=tk.LEFT, padx=10)
      
    """def exist_id_cliente(self, id_cliente):
            schemacs = pymysql.connect(host="localhost", user="root", password="123456", database="schemacs")
            cursor = schemacs.cursor()
            cursor.execute("SELECT * FROM cliente WHERE ID=%s", (id_cliente,))
            result = cursor.fetchone()
            schemacs.close()
            if result:
                return True
    """

    def exist_id (self, id_cliente, id_producto):
        schemacs = pymysql.connect(host="localhost", user="root", password="123456", database="schemacs")
        cursor = schemacs.cursor()
        cursor.execute("SELECT * FROM cliente, producto WHERE cliente.ID=%s AND producto.ID=%s", (id_cliente, id_producto))
        result = cursor.fetchone()
        schemacs.close()
        if result:
            return True
            
    def guardar_datos(self):
        if self.ID.get() == "" or self.ID_cliente.get() == "" or self.ID_producto.get() == "":
            messagebox.showerror("Control de Stock", "Ingrese información en todos los campos")
        else:
            
            codigo_cliente = self.ID_cliente.get()
            codigo_producto = self.ID_producto.get()
            
            if not self.exist_id(codigo_cliente, codigo_producto):
                messagebox.showerror("Control de Stock", "No existe ese ID de cliente o producto")
                return
            
            fecha_seleccionada = self.Fecha_compra.get_date()
            fecha_mysql = fecha_seleccionada.strftime('%Y-%m-%d')
            
            schemacs = pymysql.connect(host="localhost", user="root", password="123456", database="schemacs")
            cursor = schemacs.cursor()

            cursor.execute("INSERT INTO compra (id_cliente, id_producto, cantidad, fecha_compra) VALUES (%s, %s, %s, %s)", (
                codigo_cliente,
                codigo_producto,
                self.Cantidad.get(),
                fecha_mysql,
            ))
            messagebox.showinfo("Datos Completados", "Se agregaron correctamente")

            schemacs.commit()
            schemacs.close()

            if self.callback:
                self.callback()

            self.parent_compra.actualizar()
            self.dialog.destroy()
    
    
    def modificar_datos(self):
        if self.ID.get() == "" or self.ID_cliente.get() == "" or self.ID_producto.get() == "":
            messagebox.showerror("Control de Stock", "Ingrese información en todos los campos")
        else:
            codigo_cliente = self.ID_cliente.get()
            codigo_producto = self.ID_producto.get()
            
            if not self.exist_id(codigo_cliente, codigo_producto):
                messagebox.showerror("Control de Stock", "No existe ese ID de cliente o producto")
                return
            
            schemacs = pymysql.connect(host="localhost", user="root", password="123456", database="schemacs")
            cursor = schemacs.cursor()
            
            fecha_seleccionada = self.Fecha_compra.get_date()
            fecha_mysql = fecha_seleccionada.strftime('%Y-%m-%d')
            
            cursor.execute("UPDATE compra SET id_cliente=%s, id_producto=%s, Cantidad=%s, Fecha_compra=%s WHERE ID=%s", (
                codigo_cliente,
                codigo_producto,
                self.Cantidad.get(),
                fecha_mysql,
                self.ID.get(),
            ))
            messagebox.showinfo("Datos Completados", "Se actualizaron correctamente")
            
            schemacs.commit()
            schemacs.close()

            if self.callback:
                self.callback()

            self.parent_compra.actualizar()
            self.dialog.destroy()           
