import tkinter as tk

class CButton:
    def __init__(self, canvas, x, y, w, h, text, command, bg="#C28E44", fg="white"):
        self.canvas = canvas
        self.x, self.y, self.w, self.h = x, y, w, h
        self.text, self.command, self.bg, self.fg = text, command, bg, fg

    def draw(self):
        tag = f"btn_{self.text}_{self.x}_{self.y}"
        self.canvas.create_rectangle(self.x, self.y, self.x + self.w, self.y + self.h, fill=self.bg, outline="", tags=tag)
        self.canvas.create_text(self.x + (self.w/2), self.y + (self.h/2), text=self.text, fill=self.fg, font=("Roboto", 10, "bold"), tags=tag)
        self.canvas.tag_bind(tag, "<Button-1>", lambda e: self.command())
        self.canvas.tag_bind(tag, "<Enter>", lambda e: self.canvas.config(cursor="hand2"))
        self.canvas.tag_bind(tag, "<Leave>", lambda e: self.canvas.config(cursor=""))

class CInput:
    def __init__(self, canvas, x, y, w, h, placeholder, is_password=False):
        self.canvas, self.x, self.y, self.w, self.h = canvas, x, y, w, h
        self.placeholder, self.is_password = placeholder, is_password
        self.entry = None

    def draw(self):
        self.canvas.create_rectangle(self.x, self.y, self.x + self.w, self.y + self.h, fill="#1A1A1A", outline="#C28E44")
        self.entry = tk.Entry(self.canvas.master, bg="#1A1A1A", fg="white", insertbackground="white", bd=0, highlightthickness=0, show="*" if self.is_password else "")
        self.canvas.create_window(self.x + (self.w/2), self.y + (self.h/2), window=self.entry, width=self.w - 10, height=self.h - 10)

    def get_value(self):
        return self.entry.get() if self.entry else ""