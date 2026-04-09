import customtkinter as ctk
from app.views.styles import FONT_TITLE

class UserHeader(ctk.CTkFrame):
    def __init__(self, master, username, **kwargs):
        # Aseguramos que el height se mantenga
        super().__init__(master, fg_color="transparent", height=60, **kwargs)
        self.pack_propagate(False)

        ctk.CTkLabel(
            self, 
            text=f"Hola, {username}!", 
            font=(FONT_TITLE[0], 22, "bold"), 
            text_color="white"
        ).pack(side="left")
        
        self.avatar = ctk.CTkLabel(
            self, text="👤", font=("Roboto", 24), 
            fg_color="#252525", width=45, height=45, corner_radius=22
        )
        self.avatar.pack(side="right")