import customtkinter as ctk

class ScrollableList(ctk.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)

    def clear(self):
        for child in self.winfo_children():
            child.destroy()

    def render_items(self, items, row_class, on_action_callback):
        """
        items: lista de diccionarios (datos)
        row_class: La clase del componente fila (ej: ProductRow)
        on_action_callback: Función a ejecutar al interactuar
        """
        for item in items:
            row = row_class(self, item, on_action_callback)
            row.pack(fill="x", pady=5, padx=5)