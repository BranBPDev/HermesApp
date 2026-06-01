import tkinter as tk
from app.gui.components.widgets.visual_elements import CButton, CInput
from app.gui.styles.styles import COLOR_BG_DARK
from app.managers.tag_manager import TagManager

class SearchBar(tk.Frame):
    def __init__(self, master, on_search, **kwargs):
        super().__init__(master, bg=COLOR_BG_DARK, height=60)
        self.on_search = on_search
        self.tm = TagManager()
        self.pack_propagate(False)
        
        self.canvas = tk.Canvas(self, bg=COLOR_BG_DARK, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        
        self.inp = CInput(self.canvas, "BUSCAR PRODUCTO", "Escribe el nombre del producto...")
        self.btn = CButton(self.canvas, "BUSCAR", self._trigger_search)
        
        if hasattr(self.inp, 'entry'):
            self.inp.entry.bind("<KeyRelease>", self._on_key_release)
            # Cerrar sugerencias al salir del foco
            self.inp.entry.bind("<FocusOut>", lambda e: self.master.after(200, self._hide_suggestions))
            
        self.suggestion_list = None
        
        self.canvas.bind("<Configure>", lambda e: self.draw())
        self.master.winfo_toplevel().bind("<Return>", lambda e: self._trigger_search())

    def _on_key_release(self, event):
        if event.keysym in ('Up', 'Down', 'Return'): return
        query = self.get_query()
        if len(query) >= 1:
            suggestions = self.tm.get_suggestions(query)
            if suggestions: self._show_suggestions(suggestions)
            else: self._hide_suggestions()
        else: self._hide_suggestions()

    def _show_suggestions(self, suggestions):
        self._hide_suggestions() # Asegurar que se limpia antes
        
        # Crear ventana flotante
        self.suggestion_list = tk.Toplevel(self)
        self.suggestion_list.overrideredirect(True)
        self.suggestion_list.attributes("-topmost", True)
        
        # Posicionar exactamente debajo del input
        x = self.inp.entry.winfo_rootx()
        y = self.inp.entry.winfo_rooty() + self.inp.entry.winfo_height()
        w = 400
        h = min(len(suggestions) * 30, 200)
        
        self.suggestion_list.geometry(f"{w}x{h}+{x}+{y}")
        
        listbox = tk.Listbox(
            self.suggestion_list, 
            bg="#2d2d2d", fg="white", 
            selectbackground="#007acc", selectforeground="white",
            relief="flat", borderwidth=0, highlightthickness=0,
            font=("Arial", 11)
        )
        listbox.pack(fill="both", expand=True)
        
        for s in suggestions:
            listbox.insert(tk.END, f"  {s}")
            
        listbox.bind("<<ListboxSelect>>", self._on_select)
        self.suggestion_list.listbox = listbox

    def _hide_suggestions(self):
        if self.suggestion_list:
            self.suggestion_list.destroy()
            self.suggestion_list = None

    def _on_select(self, event):
        lb = event.widget
        if lb.curselection():
            selection = lb.get(lb.curselection()).strip()
            self.set_query(selection)
            self._hide_suggestions()
            self._trigger_search()

    def set_query(self, text):
        if hasattr(self.inp, 'set'): self.inp.set(text)
        elif hasattr(self.inp, 'entry'):
            self.inp.entry.delete(0, 'end')
            self.inp.entry.insert(0, text)
            self.inp.placeholder_active = False

    def _trigger_search(self):
        self._hide_suggestions()
        query = self.get_query()
        if query: self.on_search(query)

    def get_query(self):
        return self.inp.get()

    def draw(self):
        self.canvas.delete("all")
        w = self.canvas.winfo_width()
        self.inp.draw(30, 7, w=w-200)
        self.btn.draw(w-150, 5, w=120)