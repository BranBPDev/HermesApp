import tkinter as tk
from app.utils.logger_util import HermesLogger
from app.gui.styles.styles import (
    COLOR_PRIMARY, COLOR_PRIMARY_HOVER, COLOR_PRIMARY_ACTIVE, COLOR_TEXT_MAIN, 
    COLOR_TEXT_INACTIVE, COLOR_INPUT_BG, COLOR_BADGE_BG, FONT_LABEL, FONT_INPUT, 
    FONT_BADGE, FONT_BTN, INPUT_W, INPUT_H, BADGE_W, BADGE_H, 
    BTN_W, BTN_H, CORNER_RADIUS
)

class ShapeDrawer:
    @staticmethod
    def rounded_rect(canvas, x, y, w, h, r, **kwargs):
        r = min(r, h/2)
        points = [x+r, y, x+w-r, y, x+w, y, x+w, y+r, x+w, y+h-r, x+w, y+h, 
                  x+w-r, y+h, x+r, y+h, x, y+h, x, y+h-r, x, y+r, x, y]
        return canvas.create_polygon(points, **kwargs, smooth=True, splinesteps=32)

class CBadge:
    def __init__(self, canvas, text, color=COLOR_TEXT_INACTIVE):
        self.canvas, self.text, self.color = canvas, text, color
    def draw(self, x, y, w=BADGE_W, h=BADGE_H):
        ShapeDrawer.rounded_rect(self.canvas, x, y, w, h, 10, fill=COLOR_BADGE_BG)
        self.canvas.create_text(x + 12, y + (h/2), text=self.text, fill=self.color, font=FONT_BADGE, anchor="w")

class CInput:
    def __init__(self, canvas, label, placeholder, is_pass=False, callback=None):
        self.canvas, self.label, self.placeholder, self.is_pass, self.callback = canvas, label, placeholder, is_pass, callback
        self.placeholder_active = True
        self.rect_id = None
        self.entry = tk.Entry(canvas.master, bg=COLOR_INPUT_BG, fg=COLOR_TEXT_INACTIVE, 
                              insertbackground=COLOR_PRIMARY, bd=0, highlightthickness=0, font=FONT_INPUT)
        self.entry.insert(0, placeholder)
        self.entry.bind("<FocusIn>", self._focus_in)
        self.entry.bind("<FocusOut>", self._focus_out)

    def draw(self, x, y, show_pass=False, w=INPUT_W, h=INPUT_H):
        tag = f"input_bg_{id(self)}"
        if self.label:
            self.canvas.create_text(x + 5, y - 15, text=self.label, fill=COLOR_TEXT_MAIN, font=FONT_LABEL, anchor="w")
        self.rect_id = ShapeDrawer.rounded_rect(self.canvas, x, y, w, h, CORNER_RADIUS, fill=COLOR_INPUT_BG, outline="", tags=tag)
        
        entry_w = w - (65 if self.is_pass else 35)
        if self.is_pass: self.entry.configure(show="" if show_pass or self.placeholder_active else "*")
        self.canvas.create_window(x + (entry_w/2) + 18, y + (h/2), window=self.entry, width=entry_w, height=h-12)

        if self.is_pass and self.callback:
            eye_tag = f"eye_{id(self)}"
            self.canvas.create_text(x + w - 22, y + (h/2), text="👁" if show_pass else "🔒", 
                                    fill=COLOR_PRIMARY, font=FONT_INPUT, tags=eye_tag)
            self.canvas.tag_bind(eye_tag, "<Button-1>", lambda e: self.callback())

    def _focus_in(self, e):
        self.canvas.itemconfig(self.rect_id, outline=COLOR_PRIMARY, width=1)
        if self.placeholder_active:
            self.entry.delete(0, tk.END); self.entry.configure(fg=COLOR_TEXT_MAIN)
            self.placeholder_active = False
            if self.is_pass: self.entry.configure(show="*")

    def _focus_out(self, e):
        self.canvas.itemconfig(self.rect_id, outline="")
        if not self.entry.get():
            self.entry.configure(show=""); self.entry.insert(0, self.placeholder)
            self.entry.configure(fg=COLOR_TEXT_INACTIVE); self.placeholder_active = True

    def get(self): return "" if self.placeholder_active else self.entry.get()

class CButton:
    def __init__(self, canvas, text, command):
        self.canvas, self.text, self.command = canvas, text, command
        self.rect_id = None
        self.log = HermesLogger.get_logger("CBUTTON")

    def draw(self, x, y, w=BTN_W, h=BTN_H):
        tag = f"btn_{id(self)}"
        self.rect_id = ShapeDrawer.rounded_rect(self.canvas, x, y, w, h, CORNER_RADIUS, fill=COLOR_PRIMARY, tags=tag)
        self.canvas.create_text(x + (w/2), y + (h/2), text=self.text, fill=COLOR_TEXT_MAIN, font=FONT_BTN, tags=tag, state="disabled")
        
        self.canvas.tag_bind(tag, "<Enter>", lambda e: self.canvas.itemconfig(self.rect_id, fill=COLOR_PRIMARY_HOVER))
        self.canvas.tag_bind(tag, "<Leave>", lambda e: self.canvas.itemconfig(self.rect_id, fill=COLOR_PRIMARY))
        self.canvas.tag_bind(tag, "<Button-1>", self._on_click)
        self.canvas.tag_bind(tag, "<ButtonRelease-1>", lambda e: self.canvas.itemconfig(self.rect_id, fill=COLOR_PRIMARY_HOVER))

    def _on_click(self, e):
        try:
            self.canvas.itemconfig(self.rect_id, fill=COLOR_PRIMARY_ACTIVE)
            self.command()
        except Exception as ex:
            self.log.error(f"Error al ejecutar comando del botón {self.text}: {ex}")