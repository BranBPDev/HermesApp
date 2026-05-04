import tkinter as tk
from app.gui.styles.styles import COLOR_BG_DARK, COLOR_PRIMARY, FONT_LABEL

class FeedbackToast(tk.Frame):
    def __init__(self, master, **kwargs):
        # Fondo transparente o igual al del contenedor para que no se note el recuadro
        super().__init__(master, bg=COLOR_BG_DARK, height=30)
        self.pack_propagate(False)
        
        self.canvas = tk.Canvas(self, bg=COLOR_BG_DARK, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.message = ""

    def show(self, text, duration=3000):
        """Muestra el mensaje y lo borra tras el tiempo indicado"""
        self.message = text
        self.draw()
        # Programar la limpieza
        self.after(duration, self.clear)

    def clear(self):
        self.message = ""
        self.draw()

    def draw(self):
        self.canvas.delete("all")
        if not self.message:
            return
            
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        
        # Dibujamos el texto centrado como en tu código original
        self.canvas.create_text(
            w/2, h/2, 
            text=self.message, 
            fill=COLOR_PRIMARY, 
            font=FONT_LABEL, 
            anchor="center"
        )