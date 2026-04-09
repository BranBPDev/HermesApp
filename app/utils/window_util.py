def center_window(window, width, height, resizable=False):
    """Ajusta el tamaño, centra la ventana en pantalla y define si es redimensionable."""
    window.update_idletasks()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry(f"{width}x{height}+{x}+{y}")
    window.resizable(resizable, resizable)