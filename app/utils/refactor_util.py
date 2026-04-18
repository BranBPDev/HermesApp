import re

class HermesRefactorer:
    @staticmethod
    def get_normalized_data(name: str, price: float, unit_type_raw: str = None):
        """
        ORDEN LÓGICO:
        1. Cálculo de normalización (Precio y Cantidad).
        2. Cambio de etiqueta de unidad (Al final).
        """
        if not price or not isinstance(price, (int, float)): 
            return 0.0, 0.0, 'ud'

        name_clean = name.lower().replace(',', '.')
        raw_clean = (unit_type_raw or "").lower().strip()
        
        # --- PASO 1: CÁLCULO DE NORMALIZACIÓN ---
        price_norm = price
        factor = 1.0
        # Usamos una variable interna para detectar el tipo de magnitud
        magnitud = "unidad" 

        # Si es docena, calculamos el precio por unidad individual (precio / 12)
        if raw_clean == 'la docena':
            price_norm = round(price / 12, 2)
            factor = 12.0
            magnitud = "unidad"
        else:
            # Buscamos patrones de peso/volumen (ej: 300ml, 1kg, 2x125g)
            unit_pattern = r'(\d+[\.]?\d*)\s*(ml|cl|l(?:itros)?|kg|kilo(?:s)?|g(?:r(?:amos)?)?)'
            pack_match = re.search(r'(\d+)\s*[xX]\s*' + unit_pattern, name_clean)
            
            qty_encontrada = 0.0
            texto_unidad = ""

            if pack_match:
                qty_encontrada = float(pack_match.group(1)) * float(pack_match.group(2))
                texto_unidad = pack_match.group(3)
            else:
                single_match = re.search(unit_pattern, name_clean)
                if single_match:
                    qty_encontrada = float(single_match.group(1))
                    texto_unidad = single_match.group(2)

            if qty_encontrada > 0:
                factor = qty_encontrada
                # Lógica para determinar si el factor debe convertirse a base (L o Kg)
                if any(u in texto_unidad for u in ['l', 'litro']):
                    magnitud = "litro"
                    if 'ml' in texto_unidad: factor = qty_encontrada / 1000
                    elif 'cl' in texto_unidad: factor = qty_encontrada / 100
                elif any(u in texto_unidad for u in ['g', 'kg', 'kilo']):
                    magnitud = "kilo"
                    if texto_unidad == 'g' or 'gramo' in texto_unidad: factor = qty_encontrada / 1000
                
                price_norm = round(price / factor, 2) if factor > 0 else price
            else:
                # Si no hay match de texto, miramos el unit_type_raw para saber la magnitud
                if 'kilo' in raw_clean: magnitud = "kilo"
                elif 'litro' in raw_clean: magnitud = "litro"

        # --- PASO 2: CAMBIO DE TIPO DE UNIDAD (ESTRICTAMENTE AL FINAL) ---
        # Ahora que ya tenemos los cálculos hechos, mapeamos a tus etiquetas finales
        if magnitud == "kilo":
            final_unit = "kg"
        elif magnitud == "litro":
            final_unit = "L"
        else:
            final_unit = "ud"

        return price_norm, round(factor, 3), final_unit