from tkinter import messagebox
import pymysql

class ConexionDB:
    def __init__(self,parent):
        self.parent = parent
        self.conexion= pymysql.connect(host="localhost", user="root", password="123456", database="schemacs")
        self.cursor= self.conexion.cursor()
        
    def close(self):
        self.conexion.commit()
        self.conexion.close()
        
    def eliminar_cliente(self, values):
        cliente_id = values[0]  # Accede al primer elemento de la tupla 'values'
        self.cursor.execute("DELETE FROM cliente WHERE ID = %s", (cliente_id,))
        self.conexion.commit()  # Realiza el commit después de la operación de eliminación
        messagebox.showinfo("Cliente Eliminado", "El cliente ha sido eliminado exitosamente.")
        
    def consulta_cliente(self, q2):
        query = "SELECT ID, Nombre, Apellido, Numero_contacto FROM cliente WHERE Nombre LIKE '%" + q2 + "%' OR Apellido LIKE '%" + q2 + "%' OR ID LIKE '%" + q2 + "%' "
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        self.parent.vista(rows)
        
    def actualizar_cliente(self):
        query = "SELECT ID, Nombre, Apellido, Numero_contacto FROM cliente"
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        self.parent.vista(rows)
        
    def eliminar_producto(self, values):
        producto_id = values[0]  # Accede al primer elemento de la tupla 'values'
        self.cursor.execute("DELETE FROM producto WHERE ID = %s", (producto_id,))
        self.conexion.commit()  # Realiza el commit después de la operación de eliminación
        messagebox.showinfo("producto Eliminado", "El producto ha sido eliminado exitosamente.")
        
    def consulta_producto(self, q2):
        query = "SELECT ID, Nombre, Cantidad, Fecha_vencimiento FROM producto WHERE Nombre LIKE '%" + q2 + "%' OR Cantidad LIKE '%" + q2 + "%' OR ID LIKE '%" + q2 + "%' "
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        self.parent.vista(rows)
        
    def actualizar_producto(self):
        query = "SELECT ID, Nombre, Cantidad, Fecha_vencimiento FROM producto"
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        self.parent.vista(rows)
    
    def eliminar_compra(self, values):
        compra_id = values[0]  # Accede al primer elemento de la tupla 'values'
        self.cursor.execute("DELETE FROM compra WHERE ID = %s", (compra_id,))
        self.conexion.commit()  # Realiza el commit después de la operación de eliminación
        messagebox.showinfo("compra Eliminado", "La compra ha sido eliminado exitosamente.")
    
    def actualizar_compra(self):
        query = "SELECT ID, id_cliente, id_producto, fecha_compra, cantidad FROM compra"
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        self.parent.vista(rows)