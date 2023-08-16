from tkinter import *
from tkinter.messagebox import *
from tkinter import messagebox as Messagebox
import sqlite3
from tkinter import ttk
import re


def conexion():
    con = sqlite3.connect("mibase2.db")
    return con

def crear_tabla():
    con = conexion()
    cursor = con.cursor()
    sql = """CREATE TABLE   Concesionaria
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
             modelo varchar(20) NOT NULL,
             marca varchar(20),
             año varchar(20))
    """
    cursor.execute(sql)
    con.commit()


try:
    conexion()
    crear_tabla()
except:
    print("Hay un error")


def alta(modelo, marca,año, tree):
    cadena = modelo
    patron = "^[A-Za-z0-9]*$"  # regex para validacion de ingreso alfabetico 
    if re.match(patron, cadena):
        print(marca, modelo, año)
        con = conexion()
        cursor = con.cursor()
        data = (marca, modelo, año)
        sql = (
            "INSERT INTO Concesionaria(modelo , marca , año) VALUES(?, ?, ?)"
        )
        cursor.execute(sql, data)
        con.commit()
        print("Automovil en alta todo ok")
        actualizar_treeview(tree)
    else:
        showerror(
            "Error de ingreso en el campo marca",
            "El campo solo admite caracteres alfanuméricos",
        )


def borrar(tree):
    valor = tree.selection()
    print(valor)  # ('I005',)
    item = tree.item(valor)
    print(
        item
    )  # {'text': 5, 'image': '', 'values': ['daSDasd', '13.0', '2.0'], 'open': 0, 'tags': ''}
    print(item["text"])
    mi_id = item["text"]

    con = conexion()
    cursor = con.cursor()
    # mi_id = int(mi_id)
    data = (mi_id,)
    sql = "DELETE FROM Concesionaria WHERE id = ?;"
    cursor.execute(sql, data)
    con.commit()
    tree.delete(valor)


def actualizar_treeview(mitreview):
    records = mitreview.get_children()
    for element in records:
        mitreview.delete(element)

    sql = "SELECT * FROM Concesionaria ORDER BY id ASC"
    con = conexion()
    cursor = con.cursor()
    datos = cursor.execute(sql)

    resultado = datos.fetchall()
    for fila in resultado:
        print(fila)
        mitreview.insert("", 0, text=fila[0], values=(fila[1], fila[2], fila[3]))


# ####################################################
# VISTA
# ###################################################

master = Tk()
master.title("Mi Concesionaria")

titulo = Label(
    master,
    text="Ingrese los datos del vehiculo",
    bg="DarkOrchid3",
    fg="thistle1",
    height=1,
    width=60,
)
titulo.grid(row=0, column=0, columnspan=4, padx=1, pady=1, sticky=W + E)

nombre = Label(master, text="Marca")
nombre.grid(row=1, column=0, sticky=W)
Modelo= Label(master, text="Modelo")
Modelo.grid(row=2, column=0, sticky=W)
Año = Label(master, text="Año")
Año.grid(row=3, column=0, sticky=W)


# Defino variables para tomar valores de campos de entrada
a_val, b_val, c_val = StringVar(), StringVar(), StringVar()
w_ancho = 20

entry_nombre = Entry(master, textvariable=a_val, width=w_ancho)
entry_nombre.grid(row=1, column=1)
entry_marca= Entry(master, textvariable=b_val, width=w_ancho)
entry_marca.grid(row=2, column=1)
entry_año = Entry(master, textvariable=c_val, width=w_ancho)
entry_año.grid(row=3, column=1)

"""
def funcion():
    print("Modelo del Vehiculo:", entry_nombre.get()),
    print("Marca:", entry_marca.get())
    print("Año:", entry_año.get())
"""
# --------------------------------------------------
# TREEVIEW
# --------------------------------------------------

tree = ttk.Treeview(master)
tree["columns"] = ("col1", "col2", "col3")
tree.column("#0", width=90, minwidth=50, anchor=W)
tree.column("col1", width=200, minwidth=80)
tree.column("col2", width=200, minwidth=80)
tree.column("col3", width=200, minwidth=80)
tree.heading("#0", text="ID")
tree.heading("col1", text="modelo")
tree.heading("col2", text="marca")
tree.heading("col3",  text="año")
tree.grid(row=10, column=0, columnspan=4)

def modificacion(tree, p1, l1, c1):
    valor = tree.selection()
    resultado = Messagebox.askquestion(
        "Baja", "¿Estas seguro de querer modificar vehiculo?"
    )
    if resultado == "yes":
        item = tree.item(valor)
        id_update = item["text"]
        con = conexion()
        cursor = con.cursor()
        sql = "UPDATE Concesionaria SET Marca =?, Modelo=?,Año=? WHERE id = ?;"
        datos = cursor.execute(sql,(c1, l1, p1, a_val.get(), id_update))
        con.commit()
        Messagebox.showinfo(
            "Modificado",
            "Se ha modificado por: \nVehiculo: "
            + id_update
            + "\nMarca: "
            + l1
            + "\nModelo: "
            + c1,
        )
    else:
        Messagebox.showinfo("Acción cancelada", "No se modificó el Vehiculo")




boton_alta = Button(
    master,
    text="Alta",
    command=lambda: alta(a_val.get(), b_val.get(), c_val.get(), tree),
)
boton_alta.grid(row=6, column=1)


boton_borrar = Button(master, text="Borrar", command=lambda: borrar(tree))
boton_borrar.grid(row=8, column=1)

btn_modificar = Button(master, text="Modificar", command=lambda: modificacion(tree, entry_nombre.get(), entry_marca.get(), entry_año.get()))
btn_modificar.grid(row=6, column=1, sticky=W, pady=5)

master.mainloop()
