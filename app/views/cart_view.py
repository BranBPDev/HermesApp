import customtkinter as ctk

class CartView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        
        # Estado vacío del carrito
        self.empty_label = ctk.CTkLabel(
            self, 
            text="🛒 Tu carrito está vacío", 
            font=("Roboto", 18, "bold"), 
            text_color="#666666"
        )
        self.empty_label.pack(expand=True)
        
        self.subtitle_label = ctk.CTkLabel(
            self, 
            text="Añade productos desde la búsqueda para empezar a comparar totales.", 
            font=("Roboto", 13), 
            text_color="#444444"
        )
        self.subtitle_label.pack(expand=True, pady=(0, 200)) # Ajuste visual para centrar mejor