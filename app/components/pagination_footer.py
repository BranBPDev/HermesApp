import customtkinter as ctk
from app.views.styles import COLOR_PRIMARY, FONT_REGULAR

class PaginationFooter(ctk.CTkFrame):
    def __init__(self, master, command_callback, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.callback = command_callback

        self.btn_load_more = ctk.CTkButton(
            self, 
            text="MOSTRAR MÁS RESULTADOS", 
            fg_color="transparent", 
            text_color=COLOR_PRIMARY,
            hover_color="#2d2d2d",
            font=FONT_REGULAR,
            command=self.callback
        )
        # No se empaqueta por defecto, la vista decidirá cuándo mostrarlo
        
    def show(self, has_more: bool):
        if has_more:
            self.btn_load_more.pack(pady=10)
        else:
            self.btn_load_more.pack_forget()