import re

class HermesRefactorer:

    @staticmethod
    def get_manual_tag(name: str) -> str:
        return "_temp"

    @staticmethod
    def get_normalized_data(name: str, price: float):
        """
        Retorna (price_norm, quantity, unit_type)
        Normaliza todo a kg, L o ud.
        """
        if not price or not isinstance(price, (int, float)): 
            return 0.0, 0.0, 'ud'
            
        name_clean = name.lower().replace(',', '.')
        
        # Regex para capturar peso/volumen y unidades
        unit_pattern = r'(\d+[\.]?\d*)\s*(ml|cl|l(?:itros)?|kg|kilo(?:s)?|g(?:r(?:amos)?)?)'
        pack_match = re.search(r'(\d+)\s*[xX]\s*' + unit_pattern, name_clean)
        
        total_qty = 0.0
        unit_found = ""

        if pack_match:
            total_qty = float(pack_match.group(1)) * float(pack_match.group(2))
            unit_found = pack_match.group(3)
        else:
            single_match = re.search(unit_pattern, name_clean)
            if single_match:
                total_qty = float(single_match.group(1))
                unit_found = single_match.group(2)

        # Si no hay cantidad detectable, asumimos 1 unidad
        if total_qty == 0: 
            return round(price, 2), 1.0, 'ud'

        # Lógica de conversión a Base (Kg o L)
        final_unit = 'ud'
        factor = total_qty

        if any(u in unit_found for u in ['l', 'litro']):
            final_unit = 'L'
            if 'ml' in unit_found: factor = total_qty / 1000
            elif 'cl' in unit_found: factor = total_qty / 100
        elif any(u in unit_found for u in ['g', 'kg', 'kilo']):
            final_unit = 'kg'
            if unit_found == 'g' or 'gramo' in unit_found: factor = total_qty / 1000
        
        price_norm = round(price / factor, 2) if factor > 0 else price
        return price_norm, round(factor, 3), final_unit