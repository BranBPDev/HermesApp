# app/views/styles.py

# COLORES (Variables)
COLOR_PRIMARY = "#C28E44"
COLOR_PRIMARY_HOVER = "#A67833"
COLOR_BG_DARK = "#0F0F0F"
COLOR_BG_SIDE = "#181818"
COLOR_TEXT_MAIN = "#FFFFFF"
COLOR_INPUT_BG = "#1A1A1A"
COLOR_ERROR = "#FF4444"

# FUENTES
FONT_TITLE = ("Roboto", 32, "bold")
FONT_LABEL = ("Roboto", 16, "bold")
FONT_REGULAR = ("Roboto", 12)
FONT_SM = ("Roboto", 10, "bold")

# DICCIONARIOS DE ESTILO (El "CSS")
STYLE_INPUT = {
    "height": 50,
    "fg_color": COLOR_INPUT_BG,
    "border_color": COLOR_PRIMARY,
    "border_width": 1,
    "text_color": "white",
    "placeholder_text_color": "#666666",
    "corner_radius": 8
}

STYLE_BUTTON_PRIMARY = {
    "height": 55,
    "fg_color": COLOR_PRIMARY,
    "hover_color": COLOR_PRIMARY_HOVER,
    "text_color": "white",
    "font": FONT_LABEL,
    "cursor": "hand2",
    "corner_radius": 8
}

STYLE_LABEL_BRAND = {
    "font": FONT_SM,
    "text_color": COLOR_PRIMARY
}

COLOR_INFO_BADGE = "#2B2B2B"  # Gris oscuro para el fondo del badge
COLOR_TEXT_DIM = "#AAAAAA"    # Texto secundario

STYLE_BADGE = {
    "fg_color": COLOR_INFO_BADGE,
    "corner_radius": 12,
    "height": 30
}

STYLE_BADGE_TEXT = {
    "font": ("Roboto", 11),
    "text_color": COLOR_PRIMARY
}