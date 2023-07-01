import pymysql
import tkinter as tk
from tkinter import ttk
from cliente_dialog import ClienteDialog
from tkinter import messagebox
from pes_productos import ProductoApp


class ClienteApp:
    def __init__(self, root):
        self.wind = root
        self.wind.title("Control de Stock")
        self.wind.geometry("1000x550")
        self.wind.config(bg="indian red")
        self.wind.resizable(True, True)

        self.cuaderno1 = ttk.Notebook(self.wind)

        self.crear_pestana_clientes()
        self.crear_pestana_productos()

        self.cuaderno1.pack(fill="both", expand=True, padx=10, pady=15)

    def crear_pestana_clientes(self):
        pestana_clientes = ttk.Frame(self.cuaderno1)
        self.cuaderno1.add(pestana_clientes, text="Clientes")

        frame1 = tk.LabelFrame(pestana_clientes, text="Consulta Del Cliente", font=("calibri", ), relief=tk.SUNKEN)
        frame1.pack(fill="both", expand="yes", padx=20, pady=3)
        frame2 = tk.LabelFrame(pestana_clientes, text="Datos Del Cliente", font=("calibri", 14), relief=tk.SUNKEN)
        frame2.pack(fill="both", expand="yes", padx=20, pady=20)

        self.ID = tk.StringVar()
        self.Nombre = tk.StringVar()
        self.Apellido = tk.StringVar()
        self.Numero_contacto = tk.StringVar()

        self.trv = ttk.Treeview(frame2, columns=(1, 2, 3, 4), show="headings", height="8")
        self.trv.pack()
        self.trv.heading(1, text="ID Cliente")
        self.trv.heading(2, text="Nombre Del Cliente")
        self.trv.heading(3, text="Apellido Del Cliente")
        self.trv.heading(4, text="Número Del Cliente")
        self.trv.bind("<Double-Button-1>", self.editar_datos)

        lbl = tk.Label(frame1, text="Consulta")
        lbl.pack(side=tk.LEFT, padx=10)
        self.q = tk.StringVar()
        ent = tk.Entry(frame1, textvariable=self.q)
        ent.pack(side=tk.LEFT, padx=6)

        # Botones
        btn = tk.Button(frame2, text="Agregar", command=lambda: self.abrir_ventana_agregar_editar())
        btn.pack(side=tk.TOP)

        btn = tk.Button(frame1, text="Eliminar", command=self.eliminar)
        btn.pack(side=tk.RIGHT, padx=20)
        btn = tk.Button(frame1, text="Actualizar", command=self.actualizar)
        btn.pack(side=tk.RIGHT, padx=25)
        btn = tk.Button(frame1, text="Buscar", command=self.consulta)
        btn.pack(side=tk.LEFT, padx=6)
        btn = tk.Button(frame1, text="Restablecer", command=self.restablecer)
        btn.pack(side=tk.LEFT, padx=6)

        schemacs = pymysql.connect(host="localhost", user="root", password="123456", database="schemacs")
        cursor = schemacs.cursor()
        query = "SELECT ID, Nombre, Apellido, Numero_contacto FROM cliente"
        cursor.execute(query)
        rows = cursor.fetchall()
        self.vista(rows)
        schemacs.close()

    #Funciones
    def crear_pestana_productos(self):
        ProductoApp(self.cuaderno1)
     #Vista de la tabla
    def vista(self, rows):
        self.trv.delete(*self.trv.get_children())
        for i in rows:
            self.trv.insert('', 'end', values=i)
    
     #Verifica los datos editados
    def agregar_editar_datos(self):
        if self.ID.get() == "" or self.Nombre.get() == "" or self.Apellido.get() == "":
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
            schemacs.commit()
            schemacs.close()
            messagebox.showinfo("Datos Completados", "Se agregaron correctamente")
            self.ID.set("")
            self.Nombre.set("")
            self.Apellido.set("")
            self.Numero_contacto.set("")
            self.actualizar()
     
    def editar_datos(self, event):
        item = self.trv.focus()
        ClienteDialog(self, self.agregar_editar_datos, item)
        
    def abrir_ventana_agregar_editar(self, item=None):
        ClienteDialog(self, item)

    def actualizar(self):
        schemacs = pymysql.connect(host="localhost", user="root", password="123456", database="schemacs")
        cursor = schemacs.cursor()
        query = "SELECT ID, Nombre, Apellido, Numero_contacto FROM cliente"
        cursor.execute(query)
        rows = cursor.fetchall()
        self.vista(rows)
        schemacs.close()

    def consulta(self):
        q2 = self.q.get()
        schemacs = pymysql.connect(host="localhost", user="root", password="123456", database="schemacs")
        cursor = schemacs.cursor()
        query = "SELECT ID, Nombre, Apellido, Numero_contacto FROM cliente WHERE Nombre LIKE '%" + q2 + "%' OR Apellido LIKE '%" + q2 + "%' OR ID LIKE '%" + q2 + "%' "
        cursor.execute(query)
        rows = cursor.fetchall()
        self.vista(rows)
        schemacs.close()

    def restablecer(self):
        schemacs = pymysql.connect(host="localhost", user="root", password="123456", database="schemacs")
        cursor = schemacs.cursor()
        query = "SELECT ID, Nombre, Apellido, Numero_contacto FROM cliente"
        cursor.execute(query)
        rows = cursor.fetchall()
        self.vista(rows)
        schemacs.close()

    def eliminar(self):
        # Obtener el ID del cliente seleccionado en la tabla
        selected_item = self.trv.focus()
        values = self.trv.item(selected_item)['values']
        cliente_id = values[0]
        # Confirmar la eliminación con un cuadro de diálogo
        confirmation = messagebox.askyesno("Eliminar Cliente", "¿Está seguro que desea eliminar este cliente?")

        if confirmation:
            try:
                # Conectar a la base de datos
                schemacs = pymysql.connect(host="localhost", user="root", password="123456", database="schemacs")
                cursor = schemacs.cursor()
                # Ejecutar la consulta SQL para eliminar el cliente
                cursor.execute("DELETE FROM cliente WHERE ID = %s", (cliente_id,))
                schemacs.commit()
                # Cerrar la conexión y mostrar un mensaje de éxito
                schemacs.close()
                messagebox.showinfo("Cliente Eliminado", "El cliente ha sido eliminado exitosamente.")
                # Actualizar la tabla
                self.actualizar()
            except pymysql.Error as e:
                messagebox.showerror("Error", f"No se pudo eliminar el cliente: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ClienteApp(root)
    root.mainloop()