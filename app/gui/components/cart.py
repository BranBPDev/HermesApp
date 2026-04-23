import tkinter as tk

class Cart(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, bg="#0F0F0F")
        tk.Label(self, text="CARRITO VACÍO", fg="#444444", bg="#0F0F0F", font=("Roboto", 20)).pack(expand=True)