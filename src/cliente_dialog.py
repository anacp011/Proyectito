import tkinter as tk
from tkinter import messagebox
import pymysql

class ClienteDialog:
    def __init__(self, parent, parent_cliente, item=None, callback=None):
        self.parent = parent
        self.parent_cliente = parent_cliente
        self.callback = callback
        self.dialog = tk.Toplevel(self.parent)
        self.dialog.title("Agregar/Editar Cliente")
        self.dialog.geometry("400x250")

        frame = tk.Frame(self.dialog)
        frame.pack(pady=20)

        tk.Label(frame, text="ID Cliente:").grid(row=0, column=0, sticky="e")
        self.ID = tk.Entry(frame)
        self.ID.grid(row=0, column=1)
        tk.Label(frame, text="Nombre:").grid(row=1, column=0, sticky="e")
        self.Nombre = tk.Entry(frame)
        self.Nombre.grid(row=1, column=1)
        tk.Label(frame, text="Apellido:").grid(row=2, column=0, sticky="e")
        self.Apellido = tk.Entry(frame)
        self.Apellido.grid(row=2, column=1)
        tk.Label(frame, text="Número de contacto:").grid(row=3, column=0, sticky="e")
        self.Numero_contacto = tk.Entry(frame)
        self.Numero_contacto.grid(row=3, column=1)

        btn_frame = tk.Frame(self.dialog)
        btn_frame.pack(pady=20)

        if item:
            values = self.parent_cliente.trv.item(item, 'values')
            self.ID.insert(tk.END, values[0])
            self.Nombre.insert(tk.END, values[1])
            self.Apellido.insert(tk.END, values[2])
            self.Numero_contacto.insert(tk.END, values[3])

            tk.Button(btn_frame, text="Actualizar ", command=self.modificar_datos).pack(side=tk.LEFT, padx=10)
        else:
            tk.Button(btn_frame, text="Agregar", command=self.guardar_datos).pack(side=tk.LEFT, padx=10)

        tk.Button(btn_frame, text="Cancelar", command=self.dialog.destroy).pack(side=tk.LEFT, padx=10)

    def guardar_datos(self):
        if self.Nombre.get() == "" or self.Apellido.get() == "":
            messagebox.showerror("Control de Stock", "Ingrese información en todos los campos")
        else:
            schemacs = pymysql.connect(host="localhost", user="root", password="123456", database="schemacs")
            cursor = schemacs.cursor()

            cursor.execute("INSERT INTO cliente (Nombre, Apellido, Numero_contacto) VALUES (%s, %s, %s)", (
                self.Nombre.get(),
                self.Apellido.get(),
                self.Numero_contacto.get()
            ))
            messagebox.showinfo("Datos Completados", "Se agregaron correctamente")

            schemacs.commit()
            schemacs.close()

            if self.callback:
                self.callback()

            self.parent_cliente.restablecer()
            self.dialog.destroy()

    def modificar_datos(self):
        if self.Nombre.get() == "" or self.Apellido.get() == "":
            messagebox.showerror("Control de Stock", "Ingrese información en todos los campos")
        else:
            schemacs = pymysql.connect(host="localhost", user="root", password="123456", database="schemacs")
            cursor = schemacs.cursor()
            
            cursor.execute("UPDATE cliente SET Nombre=%s, Apellido=%s, Numero_contacto=%s WHERE ID=%s", (
                self.Nombre.get(),
                self.Apellido.get(),
                self.Numero_contacto.get(),
                self.ID.get(),
            ))
            messagebox.showinfo("Datos Completados", "Se actualizaron correctamente")
            
            schemacs.commit()
            schemacs.close()

            if self.callback:
                self.callback()

            self.parent_cliente.restablecer()
            self.dialog.destroy()           