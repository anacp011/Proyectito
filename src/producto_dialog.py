import tkinter as tk
from tkinter import messagebox
from tkcalendar import *
from tkcalendar import DateEntry
from datetime import datetime
import pymysql

class ProductoDialog:
    def __init__(self, parent, item=None, callback=None):
        self.parent = parent
        self.callback = callback
        self.dialog = tk.Toplevel(parent.parent.wind)
        self.dialog.title("Agregar/Editar Producto")
        self.dialog.geometry("400x250")

        frame = tk.Frame(self.dialog)
        frame.pack(pady=40)

        tk.Label(frame, text="ID Producto:").grid(row=0, column=0, sticky="e")
        self.ID = tk.Entry(frame)
        self.ID.grid(row=0, column=1)
        tk.Label(frame, text="Nombre:").grid(row=1, column=0, sticky="e")
        self.Nombre = tk.Entry(frame)
        self.Nombre.grid(row=1, column=1)
        
        tk.Label(frame, text="Cantidad:").grid(row=2, column=0, sticky="e")
        self.Cantidad = tk.Entry(frame)
        self.Cantidad.grid(row=2, column=1)

        tk.Label(frame, text="Fecha de vencimiento:").grid(row=3, column=0, sticky="e")
        
        if item: 
            self.Fecha_vencimiento = DateEntry(frame)
        else:    
            self.Fecha_vencimiento = DateEntry(frame, date_pattern='yyyy/mm/dd')
        
        self.Fecha_vencimiento.grid(row=3, column=1)
        
        btn_frame = tk.Frame(self.dialog)
        btn_frame.pack(pady=20)

        if item:
            values = self.parent.trv.item(item, 'values')
            self.ID.insert(tk.END, values[0])
            self.Nombre.insert(tk.END, values[1])
            self.Cantidad.insert(tk.END, values[2])
            self.Fecha_vencimiento.delete(0, tk.END)
            self.Fecha_vencimiento.insert(tk.END, values[3])

            tk.Button(btn_frame, text="Actualizar", command=self.modificar_datos).pack(side=tk.LEFT, padx=10)
        else:
            tk.Button(btn_frame, text="Agregar", command=self.guardar_datos).pack(side=tk.LEFT, padx=10)

        tk.Button(btn_frame, text="Cancelar", command=self.dialog.destroy).pack(side=tk.LEFT, padx=10)
        


    def guardar_datos(self):
        if self.Nombre.get() == "" or self.Cantidad.get() == "":
            messagebox.showerror("Control de Stock", "Ingrese información en todos los campos")
        else:

            fecha_seleccionada = self.Fecha_vencimiento.get_date()
            fecha_mysql = fecha_seleccionada.strftime('%Y-%m-%d')
            
            schemacs = pymysql.connect(host="localhost", user="root", password="123456", database="schemacs")
            cursor = schemacs.cursor()

            cursor.execute("INSERT INTO producto (Nombre, Cantidad, Fecha_vencimiento) VALUES (%s, %s, %s)", (
                self.Nombre.get(),
                self.Cantidad.get(),
                fecha_mysql,
            ))
            messagebox.showinfo("Datos Completados", "Se agregaron correctamente")

            schemacs.commit()
            schemacs.close()

            if self.callback:
                self.callback()

            self.parent.restablecer()
            self.dialog.destroy()
    
    
    def modificar_datos(self):
        if self.Nombre.get() == "" or self.Cantidad.get() == "":
            messagebox.showerror("Control de Stock", "Ingrese información en todos los campos")
        else:
            schemacs = pymysql.connect(host="localhost", user="root", password="123456", database="schemacs")
            cursor = schemacs.cursor()
            
            fecha_seleccionada = self.Fecha_vencimiento.get_date()
            fecha_mysql = fecha_seleccionada.strftime('%Y-%m-%d')
            
            cursor.execute("UPDATE producto SET Nombre=%s, Cantidad=%s, Fecha_vencimiento=%s WHERE ID=%s", (
                self.Nombre.get(),
                self.Cantidad.get(),
                fecha_mysql,
                self.ID.get(),
            ))
            messagebox.showinfo("DATOS Completados", "Se actualizaron correctamente")
            
            schemacs.commit()
            schemacs.close()

            if self.callback:
                self.callback()

            self.parent.restablecer()
            self.dialog.destroy()           
            
    