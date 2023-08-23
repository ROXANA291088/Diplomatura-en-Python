import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import re
import time

class ConcesionariaModel:
    def __init__(self):
        self.con = sqlite3.connect("mibase2.db")
        self.crear_tabla()

    def crear_tabla(self):
        cursor = self.con.cursor()
        sql = """CREATE TABLE IF NOT EXISTS Concesionaria
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 modelo varchar(20) NOT NULL,
                 marca varchar(20),
                 año varchar(20))
        """
        cursor.execute(sql)
        self.con.commit()

    def alta(self, modelo, marca, año):
        cadena = modelo
        patron = "^[A-Za-z0-9]*$"
        if re.match(patron, cadena):
            cursor = self.con.cursor()
            data = (marca, modelo, año)
            sql = "INSERT INTO Concesionaria(modelo , marca , año) VALUES(?, ?, ?)"
            cursor.execute(sql, data)
            self.con.commit()
            return True
        else:
            return False
        
    def modificar(self, mi_id, marca, modelo, año):
        cursor = self.con.cursor()
        sql = "UPDATE Concesionaria SET marca=?, modelo=?, año=? WHERE id=?"
        data = (marca, modelo, año, mi_id)
        cursor.execute(sql, data)
        self.con.commit()
    

    def borrar(self, mi_id):
        cursor = self.con.cursor()
        data = (mi_id,)
        sql = "DELETE FROM Concesionaria WHERE id = ?;"
        cursor.execute(sql, data)
        self.con.commit()

    def obtener_vehiculos(self):
        cursor = self.con.cursor()
        sql = "SELECT * FROM Concesionaria ORDER BY id ASC"
        datos = cursor.execute(sql)
        return datos.fetchall()

class ConcesionariaView(tk.Tk):
    def __init__(self, model):
        super().__init__()
        self.title("Mi Concesionaria")

        self.model = model

        self.titulo = tk.Label(
            self,
            text="Ingrese los datos del vehiculo",
            bg="DarkOrchid3",
            fg="thistle1",
            height=1,
            width=60,
        )
        self.titulo.grid(row=0, column=0, columnspan=4, padx=1, pady=1, sticky=tk.W + tk.E)

        self.nombre = tk.Label(self, text="Marca")
        self.nombre.grid(row=1, column=0, sticky=tk.W)
        self.modelo = tk.Label(self, text="Modelo")
        self.modelo.grid(row=2, column=0, sticky=tk.W)
        self.año = tk.Label(self, text="Año")
        self.año.grid(row=3, column=0, sticky=tk.W)

        self.a_val, self.b_val, self.c_val = tk.StringVar(), tk.StringVar(), tk.StringVar()
        w_ancho = 20

        self.entry_nombre = tk.Entry(self, textvariable=self.a_val, width=w_ancho)
        self.entry_nombre.grid(row=1, column=1)
        self.entry_marca = tk.Entry(self, textvariable=self.b_val, width=w_ancho)
        self.entry_marca.grid(row=2, column=1)
        self.entry_año = tk.Entry(self, textvariable=self.c_val, width=w_ancho)
        self.entry_año.grid(row=3, column=1)

        self.tree = ttk.Treeview(self)
        self.tree["columns"] = ("col1", "col2", "col3")
        self.tree.column("#0", width=90, minwidth=50, anchor=tk.W)
        self.tree.column("col1", width=200, minwidth=80)
        self.tree.column("col2", width=200, minwidth=80)
        self.tree.column("col3", width=200, minwidth=80)
        self.tree.heading("#0", text="ID")
        self.tree.heading("col1", text="modelo")
        self.tree.heading("col2", text="marca")
        self.tree.heading("col3", text="año")
        self.tree.grid(row=10, column=0, columnspan=4)

        self.actualizar_treeview()

        self.boton_alta = tk.Button(
            self,
            text="Alta",
            command=self.alta,
        )
        self.boton_alta.grid(row=6, column=1)

        self.boton_borrar = tk.Button(self, text="Borrar", command=self.borrar)
        self.boton_borrar.grid(row=8, column=1)
        
        self.boton_modificar = tk.Button(
            self,
            text="Modificar",
            command=self.modificar,
        )
        self.boton_modificar = tk.Button(self, text="Modificar", command=self.boton_modificar)
        self.boton_modificar.grid(row=6, column=2, sticky=tk.W, pady=5)


        self.boton_borrar.config(command=self.borrar)
        self.boton_modificar.config(command=self.modificar)


    def alta(self):
        if self.model.alta(self.a_val.get(), self.b_val.get(), self.c_val.get()):
            self.actualizar_treeview()
            self.limpiar_campos()
        else:
            messagebox.showerror(
                "Error de ingreso en el campo marca",
                "El campo solo admite caracteres alfanuméricos",
            )

    def borrar(self):
        selected_item = self.tree.selection()
        if selected_item:
            item = self.tree.item(selected_item)
            mi_id = item["text"]
            self.model.borrar(mi_id)
            self.actualizar_treeview()

    def modificar(self):
        selected_item = self.tree.selection()
        if selected_item:
            item = self.tree.item(selected_item)
            id_update = item["text"]
            resultado = messagebox.askquestion(
                "Modificar", "¿Estás seguro de querer modificar el vehiculo?"
            )
            if resultado == "yes":
                self.model.modificar(id_update, self.b_val.get(), self.a_val.get(), self.c_val.get())
                self.actualizar_treeview()

    def actualizar_treeview(self):
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)

        resultado = self.model.obtener_vehiculos()
        for fila in resultado:
            self.tree.insert("", 0, text=fila[0], values=(fila[1], fila[2], fila[3]))

    def limpiar_campos(self):
        self.a_val.set("")
        self.b_val.set("")
        self.c_val.set("")

class ConcesionariaController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.view.boton_borrar.config(command=self.borrar)
        self.view.boton_modificar.config(command=self.modificar)
        self.view.mainloop()

    def borrar(self):
        selected_item = self.view.tree.selection()
        if selected_item:
            item = self.view.tree.item(selected_item)
            mi_id = item["text"]
            self.model.borrar(mi_id)
            self.view.actualizar_treeview()

    def modificar(self):
        selected_item = self.view.tree.selection()
        if selected_item:
            item = self.view.tree.item(selected_item)
            id_update = item["text"]
            resultado = messagebox.askquestion(
                "Modificar", "¿Estás seguro de querer modificar el vehiculo?"
            )
            if resultado == "yes":
                self.model.modificar(id_update, self.view.b_val.get(), self.view.a_val.get(), self.view.c_val.get())
                self.view.actualizar_treeview()

if __name__ == "__main__":
    concesionaria_model = ConcesionariaModel()
    concesionaria_view = ConcesionariaView(concesionaria_model)
    concesionaria_controller = ConcesionariaController(concesionaria_model, concesionaria_view)
    concesionaria_controller.view.mainloop()




# Decorador para medir el tiempo de ejecución
def medir_tiempo(func):
    def wrapper(*args, **kwargs):
        inicio = time.time()
        resultado = func(*args, **kwargs)
        fin = time.time()
        print(f"Tiempo de ejecución de {func.__name__}: {fin - inicio:.6f} segundos")
        return resultado
    return wrapper

class ConcesionariaModel:
    

    @medir_tiempo
    def alta(self, modelo, marca, año):
        cadena = modelo
        patron = "^[A-Za-z0-9]*$"
        if re.match(patron, cadena):
            cursor = self.con.cursor()
            data = (marca, modelo, año)
            sql = "INSERT INTO Concesionaria(modelo , marca , año) VALUES(?, ?, ?)"
            cursor.execute(sql, data)
            self.con.commit()
            return True
        else:
            return False
        
    @medir_tiempo
    def modificar(self, mi_id, marca, modelo, año):
        cursor = self.con.cursor()
        sql = "UPDATE Concesionaria SET marca=?, modelo=?, año=? WHERE id=?"
        data = (marca, modelo, año, mi_id)
        cursor.execute(sql, data)
        self.con.commit()
    
    @medir_tiempo
    def borrar(self, mi_id):
        cursor = self.con.cursor()
        data = (mi_id,)
        sql = "DELETE FROM Concesionaria WHERE id = ?;"
        cursor.execute(sql, data)
        self.con.commit()




