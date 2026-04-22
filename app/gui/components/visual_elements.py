import tkinter as tk
from app.gui.styles.styles import COLOR_PRIMARY, COLOR_TEXT_MAIN, FONT_REGULAR, COLOR_INPUT_BG

class CanvasComponent:
    def __init__(self, canvas, x, y, **kwargs):
        self.canvas = canvas
        self.x, self.y = x, y
        self.tags = kwargs.get("tags", "comp")

class CButton(CanvasComponent):
    def __init__(self, canvas, x, y, w, h, text, command, color=COLOR_PRIMARY):
        super().__init__(canvas, x, y)
        self.w, self.h, self.text, self.cmd = w, h, text, command
        self.tag = f"btn_{id(self)}"

    def draw(self):
        # Sombra/Borde simple
        self.canvas.create_rectangle(self.x, self.y, self.x+self.w, self.y+self.h, 
                                    fill=COLOR_PRIMARY, outline="", tags=self.tag)
        self.canvas.create_text(self.x+self.w/2, self.y+self.h/2, text=self.text, 
                               fill="white", font=FONT_REGULAR, tags=self.tag)
        # Eventos
        self.canvas.tag_bind(self.tag, "<Button-1>", lambda e: self.cmd())
        self.canvas.tag_bind(self.tag, "<Enter>", lambda e: self.canvas.config(cursor="hand2"))
        self.canvas.tag_bind(self.tag, "<Leave>", lambda e: self.canvas.config(cursor=""))

class CInput(CanvasComponent):
    def __init__(self, canvas, x, y, w, h, label="", is_password=False):
        super().__init__(canvas, x, y)
        self.w, self.h, self.label = w, h, label
        # Para inputs reales que necesiten teclado, usamos un Entry minimalista de tk
        self.entry = tk.Entry(canvas, bg=COLOR_INPUT_BG, fg="white", bd=0, 
                             highlightthickness=1, highlightbackground=COLOR_PRIMARY,
                             insertbackground="white", show="*" if is_password else "")

    def draw(self):
        if self.label:
            self.canvas.create_text(self.x, self.y-15, text=self.label, 
                                   fill="#888888", anchor="w", font=("Roboto", 10))
        # Colocamos el widget de entrada real sobre el canvas
        self.canvas.create_window(self.x + self.w/2, self.y + self.h/2, 
                                 window=self.entry, width=self.w, height=self.h)