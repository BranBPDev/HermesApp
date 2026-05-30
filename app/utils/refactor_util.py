import re

class HermesRefactorer:
    @staticmethod
    def get_normalized_data(name: str, price: float, unit_type_raw: str = None):
        if not price or not isinstance(price, (int, float)): 
            return 0.0, 1.0, 'ud'

        name_clean = name.lower().replace(',', '.')
        
        # 1. Intentar detectar formato Multiplicador (ej: 6x56 g, 24x33 cl)
        # Regex: busca numero, opcional x, numero, unidad
        pack_pattern = r'(\d+)\s*[xX]\s*(\d+(?:\.\d+)?)\s*(ml|cl|l|litros|g|gr|gramos|kg|kilo)'
        match_pack = re.search(pack_pattern, name_clean)
        
        if match_pack:
            qty = float(match_pack.group(1))
            val = float(match_pack.group(2))
            unit_str = match_pack.group(3)
            total_val = qty * val
            
            # Convertimos a unidad base
            if 'ml' in unit_str or 'cl' in unit_str or 'l' in unit_str:
                if 'ml' in unit_str: total_val /= 1000
                elif 'cl' in unit_str: total_val /= 100
                return round(price / total_val, 2), round(total_val, 3), 'L'
            elif 'g' in unit_str or 'kg' in unit_str:
                if 'g' in unit_str: total_val /= 1000
                return round(price / total_val, 2), round(total_val, 3), 'kg'

        # 2. Si no es pack, buscamos formato simple (ej: 1 litro, 500g)
        single_pattern = r'(\d+(?:\.\d+)?)\s*(ml|cl|l|litros|g|gr|gramos|kg|kilo)'
        match_single = re.search(single_pattern, name_clean)
        
        if match_single:
            val = float(match_single.group(1))
            unit_str = match_single.group(2)
            
            if 'ml' in unit_str or 'cl' in unit_str or 'l' in unit_str:
                if 'ml' in unit_str: val /= 1000
                elif 'cl' in unit_str: val /= 100
                return round(price / val, 2), round(val, 3), 'L'
            elif 'g' in unit_str or 'kg' in unit_str:
                if 'g' in unit_str: val /= 1000
                return round(price / val, 2), round(val, 3), 'kg'

        # 3. Fallback: Si no pudimos calcular nada, devolvemos el precio original
        return float(price), 1.0, 'ud'