import re
import unicodedata
from app.config.tags_config import TAG_MAPPING

class HermesRefactorer:

    @staticmethod
    def get_manual_tag(name: str) -> str:
        if not name: return "otros"
        
        name_norm = ''.join(c for c in unicodedata.normalize('NFD', name.lower())
                            if unicodedata.category(c) != 'Mn')
        
        # 1. Prioridad para PAN (si dice Pan, suele ser Pan, no Aceite)
        if "pan " in name_norm or "panecillos" in name_norm or "barras" in name_norm:
            if "molde" in name_norm: return "pan-molde"
            if "tostado" in name_norm: return "pan-tostado"
            return "pan-otros" # Tag genérico necesario

        # 2. Iteramos con Regex para buscar PALABRAS COMPLETAS (\bword\b)
        # Esto evita que 'chocolate' haga match con 'cola'
        for tag, keywords in TAG_MAPPING.items():
            for kw in keywords:
                pattern = rf'\b{re.escape(kw)}\b'
                if re.search(pattern, name_norm):
                    return tag
                    
        return "otros"

    @staticmethod
    def get_normalized_data(name: str, price: float) -> float:
        if not price or not isinstance(price, (int, float)): 
            return 0.0
            
        name_clean = name.lower().replace(',', '.')
        
        # Regex más robusto para capturar el peso en Eroski
        # Soporta: "465 g", "1kg", "1.5 l", "pack 3x65 g"
        unit_pattern = r'(\d+[\.]?\d*)\s*(ml|cl|l(?:itros)?|kg|kilo(?:s)?|g(?:r(?:amos)?)?)'
        
        pack_match = re.search(r'(\d+)\s*[xX]\s*' + unit_pattern, name_clean)
        
        total_qty = 0.0
        unit = ""

        if pack_match:
            total_qty = float(pack_match.group(1)) * float(pack_match.group(2))
            unit = pack_match.group(3)
        else:
            single_match = re.search(unit_pattern, name_clean)
            if single_match:
                total_qty = float(single_match.group(1))
                unit = single_match.group(2)

        # Si no hay cantidad, el precio normalizado es el precio base
        if total_qty == 0: return price

        # Convertir todo a base Kg o L
        if unit.startswith('k') or (unit.startswith('l') and 'ml' not in unit and 'cl' not in unit):
            factor = total_qty
        elif 'cl' in unit:
            factor = total_qty / 100
        else: # g o ml
            factor = total_qty / 1000

        return round(price / factor, 2) if factor > 0 else price