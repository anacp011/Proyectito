import tkinter as tk
from tkinter import ttk
import pymysql
from cliente_dialog import ClienteDialog
from pes_productos import ProductoApp
from pes_compra import CompraApp
from consultas_sql import ConexionDB
from tkinter import messagebox



class ClienteApp:
    def __init__(self, root):
        self.wind = root
        self.wind.title("Control de Stock")
        self.wind.geometry("1100x500")
        self.wind.config(bg="indian red")
        self.wind.resizable(True, True)

        self.cuaderno1 = ttk.Notebook(self.wind)

        self.crear_pestana_clientes()
        self.crear_pestana_productos()
        self.crear_pestana_compras()

        self.cuaderno1.pack(fill="both", expand=True, padx=10, pady=15)

    def crear_pestana_clientes(self):
        pestana_clientes = ttk.Frame(self.cuaderno1)
        self.cuaderno1.add(pestana_clientes, text="Clientes")
        
        frame1 = tk.LabelFrame(pestana_clientes, text="Consulta Del Cliente", font=("calibri",), relief=tk.SUNKEN)
        frame1.pack(fill="both", expand="yes", padx=0, pady=3)
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
        
        btn = tk.Button(frame1, text="Buscar", command=self.consulta)
        btn.pack(side=tk.LEFT, padx=6)
        btn = tk.Button(frame1, text="Restablecer", command=self.restablecer)
        btn.pack(side=tk.LEFT, padx=6)
        
        btn = tk.Button(frame2, text="Agregar", command=self.abrir_ventana_agregar_editar)
        btn.pack(side=tk.LEFT, padx=300)
        btn = tk.Button(frame2, text="Eliminar", command=self.eliminar)
        btn.pack(side=tk.LEFT)
        """btn = tk.Button(frame1, text="Actualizar", command=self.actualizar)
        btn.pack(side=tk.RIGHT, padx=25)
        """
        self.actualizar()

    def vista(self, rows):
        self.trv.delete(*self.trv.get_children())
        for i in rows:
            self.trv.insert("", "end", values=i)

    def editar_datos(self, event):
        item = self.trv.focus()
        ClienteDialog(self, item)

    def abrir_ventana_agregar_editar(self):
        ClienteDialog(self)

    def crear_pestana_productos(self):
        ProductoApp(self, self.cuaderno1)
    
    def crear_pestana_compras(self):
        CompraApp(self, self.cuaderno1)
    
    def actualizar(self):
        try:
            conexion = ConexionDB(self)  # Crea una instancia de la clase ConexionDB
            conexion.actualizar_cliente()
        except pymysql.Error as e:
            messagebox.showerror("Error", f"No se pudo actualizar la tabla de clientes: {str(e)}")
        finally:
            conexion.close()
            
    def consulta(self):
        q2 = self.q.get()
        try:
            conexion = ConexionDB(self)  # Crea una instancia de la clase ConexionDB
            conexion.consulta_cliente(q2)
        except pymysql.Error as e:
            messagebox.showerror("Error", f"No se pudo realizar la consulta de clientes: {str(e)}")
        finally:
            conexion.close()
            
    def restablecer(self):
        self.q.set("")
        self.actualizar()
    
    def eliminar(self):
        selected_item = self.trv.focus()
        if selected_item:
            values = self.trv.item(selected_item)["values"]
            
            confirmation = messagebox.askyesno("Eliminar Cliente", "¿Está seguro que desea eliminar este cliente?")
            if confirmation:
                try:
                    conexion = ConexionDB(self)  
                    conexion.eliminar_cliente(values)  
                    conexion.close() 
                    self.actualizar()
                except pymysql.Error as e:
                    messagebox.showerror("Error", f"No se pudo eliminar el cliente: {str(e)}")
        else:
            messagebox.showerror("Eliminar Cliente", "No ha seleccionado ningun cliente")
                

if __name__ == "__main__":
    root = tk.Tk()
    app = ClienteApp(root)
    root.mainloop()