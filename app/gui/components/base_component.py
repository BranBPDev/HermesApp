import tkinter as tk

class CanvasComponent:
    """Clase base para elementos dibujables en un Canvas."""
    def __init__(self, canvas, x, y, **kwargs):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.id = None
        self.tags = kwargs.get("tags", "component")

    def draw(self):
        pass

    def clear(self):
        if self.id:
            self.canvas.delete(self.id)