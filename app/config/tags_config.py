# app/config/tags_config.py

TAG_MAPPING = {
    # =========================================================================
    # 1. PRIORIDAD CRÍTICA: PRODUCTOS QUE ENGAÑAN (Suplementos y Fitness)
    # =========================================================================
    # Ponemos esto primero para que "Proteína de chocolate" no caiga en "Cola"
    "suplementos-proteina": ["whey", "proteina", "protein", "aislado de suero"],
    "sustitutos-comida": ["reemplazo", "sustitutivo"],

    # =========================================================================
    # 2. PANADERÍA Y REPOSTERÍA (Para evitar falsos positivos con Aceite/Leche)
    # =========================================================================
    "pan-blanco": ["barras de pan", "panecillos", "baguettes", "bocadillos", "barra"],
    "pan-integral": ["integral", "centeno", "multicereales"],
    "pan-molde": ["pan de molde", "burger", "brioche"],
    "pan-tostado": ["pan tostado", "biscotes", "picos", "colines"],
    "bolleria": ["croissants", "ensaimada", "muffins", "donuts", "magdalenas", "saladas surtidas"],

    # =========================================================================
    # 3. BEBIDAS (Ajustado para evitar solapamientos)
    # =========================================================================
    "refresco-cola": ["cola"], # Con \b en el refactorer, "cola" no entrará en "chocolate"
    "zumo-naranja": ["zumo de naranja", "naranja"],
    "zumo-manzana": ["zumo de manzana", "manzana"],
    "zumo-pina": ["zumo de piña", "piña"],
    "zumo-otros": ["nectar", "bebida de mango", "maracuya", "fruta de la pasion", "pomelo"],
    "agua-mineral": ["agua mineral", "agua natural"],
    "cerveza": ["cerveza", "shandy", "radler"],
    "bebida-energetica": ["monster", "red bull", "energy"],

    # =========================================================================
    # 4. LÁCTEOS, HUEVOS Y GRASAS
    # =========================================================================
    "leche-entera": ["leche entera"],
    "leche-desnatada": ["leche desnatada"],
    "leche-semidesnatada": ["leche semi", "leche semidesnatada"],
    "huevos": ["huevos", "docena"],
    "yogur-natural": ["yogur natural", "kefir", "yogur griego"],
    "mantequilla": ["mantequilla", "margarina"],
    "queso-rallado": ["queso rallado", "mozzarella rallada", "gratinar"],
    "queso-lonchas": ["queso lonchas", "havarti", "edam", "gouda"],
    "aceite-oliva-virgen": ["virgen extra", "virgen"],
    "aceite-oliva": ["aceite de oliva"], # "oliva" a secas solía dar error con el pan
    "aceite-girasol": ["girasol"],

    # =========================================================================
    # 5. DESPENSA Y BÁSICOS
    # =========================================================================
    "pasta-trigo": ["macarrones", "espaguetis", "fideos", "pasta", "tallarines", "lasaña", "noodles", "penne"],
    "arroz-blanco": ["arroz blanco", "arroz redondo", "arroz largo"],
    "legumbres": ["garbanzos", "lentejas", "alubias", "judias"],
    "harina-trigo": ["harina de trigo", "harina de fuerza"],
    "tomate-frito": ["tomate frito", "tomate triturado"],
    "azucar": ["azucar blanco", "azucar moreno"], # Evita "sin azucar" en bebidas
    "sal-mesa": ["sal fina", "sal marina", "sal de mesa"],
    "conserva-atun": ["atun", "bonito"], 
    "conserva-mejillones": ["mejillon"],
    "conserva-sardinas": ["sardin"],
    "aceitunas": ["aceituna"],
    
    # =========================================================================
    # 6. DESAYUNO Y DULCES
    # =========================================================================
    "cafe-molido": ["cafe molido", "cafe en grano"],
    "cafe-capsulas": ["cafe capsulas", "capsulas cafe"],
    "cacao-polvo": ["cacao en polvo", "nesquik", "cola cao"],
    "chocolate-tableta": ["chocolate negro", "chocolate con leche", "chocolate blanco"],
    "galletas": ["galletas maria", "galletas chocolate", "cookies"],
    "dulce-leche": ["dulce de leche"],

    # =========================================================================
    # 7. PRODUCTOS FRESCOS (Verdura/Fruta)
    # =========================================================================
    "fruta-fresca": ["sandia", "melon", "platano", "pera"],
    "verdura-fresca": ["vegetales", "ensalada", "lechuga", "zanahoria", "brocoli"]
}