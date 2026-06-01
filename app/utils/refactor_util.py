import re

class HermesRefactorer:
    @staticmethod
    def get_normalized_data(name: str, price: float, unit_type_raw: str = None):
        if not price or not isinstance(price, (int, float)): 
            return 0.0, 1.0, 'ud'

        name_clean = name.lower().replace(',', '.')
        
        # 1. Intentar detectar formato Multiplicador (ej: 6x56 g, 24x33 cl)
        pack_pattern = r'(\d+)\s*[xX]\s*(\d+(?:\.\d+)?)\s*(ml|cl|l|litros|g|gr|gramos|kg|kilo)'
        match_pack = re.search(pack_pattern, name_clean)
        
        if match_pack:
            qty = float(match_pack.group(1))
            val = float(match_pack.group(2))
            unit_str = match_pack.group(3)
            total_val = qty * val
            
            # Convertimos a unidad base
            if unit_str in ['ml', 'cl', 'l', 'litros']:
                if unit_str == 'ml': total_val /= 1000
                elif unit_str == 'cl': total_val /= 100
                return round(price / total_val, 2), round(total_val, 3), 'L'
            elif unit_str in ['g', 'gr', 'gramos', 'kg', 'kilo']:
                # Solo dividimos si es gramo, si es kg se queda igual
                if unit_str in ['g', 'gr', 'gramos']: total_val /= 1000
                return round(price / total_val, 2), round(total_val, 3), 'kg'

        # 2. Si no es pack, buscamos formato simple (ej: 1 litro, 500g)
        single_pattern = r'(\d+(?:\.\d+)?)\s*(ml|cl|l|litros|g|gr|gramos|kg|kilo)'
        match_single = re.search(single_pattern, name_clean)
        
        if match_single:
            val = float(match_single.group(1))
            unit_str = match_single.group(2)
            
            if unit_str in ['ml', 'cl', 'l', 'litros']:
                if unit_str == 'ml': val /= 1000
                elif unit_str == 'cl': val /= 100
                return round(price / val, 2), round(val, 3), 'L'
            elif unit_str in ['g', 'gr', 'gramos', 'kg', 'kilo']:
                if unit_str in ['g', 'gr', 'gramos']: val /= 1000
                return round(price / val, 2), round(val, 3), 'kg'

        # 3. Fallback: Si no pudimos calcular nada, devolvemos el precio original
        return float(price), 1.0, 'ud'