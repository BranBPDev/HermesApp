import customtkinter as ctk
from app.views.styles import COLOR_BG_DARK, COLOR_PRIMARY, COLOR_TEXT_DIM, FONT_SUBTITLE, FONT_REGULAR

class UpdateView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color=COLOR_BG_DARK, corner_radius=0)
        
        ctk.CTkLabel(self, text="NUEVA VERSIÓN DETECTADA", font=FONT_SUBTITLE, text_color=COLOR_PRIMARY).pack(pady=(150, 10))
        
        self.progress_bar = ctk.CTkProgressBar(self, width=400, progress_color=COLOR_PRIMARY)
        self.progress_bar.set(0)
        self.progress_bar.pack(pady=20)

        self.status = ctk.CTkLabel(self, text="Preparando actualización...", font=FONT_REGULAR, text_color=COLOR_TEXT_DIM)
        self.status.pack()

    def set_progress(self, val, text):
        self.after(0, lambda: self._update_ui(val, text))

    def _update_ui(self, val, text):
        self.progress_bar.set(val)
        self.status.configure(text=text)