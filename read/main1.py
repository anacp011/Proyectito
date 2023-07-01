# from tkinter import ttk
# from tkinter import *

# #Se define una clase llamada "Cliente" que representa la interfaz de usuario. 
# class Cliente:
#     # En el método __init__, se inicializa la ventana principal (self.wind)
#     # Se le da un título, un tamaño y un color de fondo.
#     def __init__(self, root):
#         self.wind = root
#         self.wind.title("Cliente")
#         self.wind.geometry("850x600")
#         self.wind.config(bg="teal")
    
#         # Se divide en dos sectores
#         frame1 = LabelFrame (self.wind, text= "Datos Del Cliente", font=("calibri", 14))
#         frame2 = LabelFrame (self.wind, text="Informacion Del Cliente", font=("calibri", 14))
#         frame1.pack(fill="both", expand="yes", padx=20, pady=15)
#         frame2.pack(fill="both", expand="yes", padx=90, pady=15)

#         # Los casilleros para inresar la info
#         lbl1 = Label(frame1, text="ID Del Cliente", width=20)
#         lbl1.grid(row=0, column=0, padx=5, pady=3)
#         self.ent1 = Entry(frame1)
#         self.ent1.grid(row=0, column=1, padx=5, pady=3)
        
#         lbl2 = Label(frame1, text="Nombre Del cliente", width=20)
#         lbl2.grid(row=1, column=0, padx=5, pady=3)
#         self.ent2 = Entry(frame1)
#         self.ent2.grid(row=1, column=1, padx=5, pady=3)

#         lbl3 = Label(frame1, text="Apellido Del Cliente", width=20)
#         lbl3.grid(row=2, column=0, padx=5, pady=3)
#         self.ent3 = Entry(frame1)
#         self.ent3.grid(row=2, column=1, padx=5, pady=3)
        
#         lbl4 = Label(frame1, text="Dirección Del Cliente", width=20)
#         lbl4.grid(row=3, column=0, padx=5, pady=3)
#         self.ent4 = Entry(frame1)
#         self.ent4.grid(row=3, column=1, padx=5, pady=3)
        
#         # Botones 
#         btn1 = Button(frame1, text="Agregar", width=12, height=2)
#         btn1.grid(row=5, column=0, padx=10, pady=10)
        
#         btn2 = Button(frame1, text="Eliminar", width=12, height=2)
#         btn2.grid(row=5, column=1, padx=10, pady=10)
        
#         btn3 = Button(frame1, text="Actualizar", width=12, height=2)
#         btn3.grid(row=5, column=2, padx=10, pady=10)
        
#         self.trv = ttk.Treeview(frame2, columns=(1,2,3,4), show="headings", height="15")
#         self.trv.pack() #crea los encabezados
#         # Encabezados:
#         self.trv.heading(1, text="ID Cliente")
#         self.trv.heading(2, text="Nombre Dell Cliente")
#         self.trv.heading(3, text="Apellido Del Cliente")
#         self.trv.heading(4, text="Direccion Del Cliente")

# if __name__== '__main__':
#     root = Tk()
#     Cliente = Cliente(root)
#     root.mainloop()
    
    