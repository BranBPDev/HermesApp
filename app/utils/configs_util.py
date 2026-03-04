# --- COMMON ---
COMMON_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'es-ES,es;q=0.9',
    'Connection': 'keep-alive',
}

# --- MERCADONA ---
MERCADONA_API_INDEX = "https://tienda.mercadona.es/api/categories/?lang=es&wh=4592"
MERCADONA_API_CAT   = "https://tienda.mercadona.es/api/categories/{cat_id}/?lang=es&wh=4592"

# --- EROSKI ---
# URL base para la carga de páginas vía AJAX (POST)
EROSKI_LOAD_URL = "https://supermercado.eroski.es/es/supermarket.productlist:loadpage?t:ac={cat}"
EROSKI_REFERER = "https://supermercado.eroski.es/es/supermercado/2059806-alimentacion/"

EROSKI_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Origin": "https://supermercado.eroski.es",
    "Referer": EROSKI_REFERER
}

EROSKI_CATEGORIES = [
    "2059806-alimentacion/2059988-aceite-vinagre-sal-harina-y-pan-rallado",
    "2059806-alimentacion/2060067-aceitunas-y-encurtidos",
    "2059806-alimentacion/2060015-conservas-de-pescado",
    "2059806-alimentacion/2060076-frutos-secos-patatas-y-snacks",
    "2059806-alimentacion/2059807-leche-batidos-y-bebidas-vegetales",
    "2059806-alimentacion/2060029-legumbres-arroz-y-pasta",
    "2059806-alimentacion/2059851-mantequilla-nata-y-cremas",
    "2059806-alimentacion/2060042-platos-preparados",
    "2059806-alimentacion/2059831-postres-lacteos-",
    "2059806-alimentacion/5000365-productos-de-dietetica",
    "2059806-alimentacion/5000364-productos-ecologicos",
    "2059806-alimentacion/2060056-salsas-y-especias",
    "2059806-alimentacion/2059818-yogures",
    "2059806-alimentacion/4000017-comida-internacional"
]

# --- GADIS ---
GADIS_API_CATEGORIES = "https://catalog.gadisline.com/api/v3/catalog/categories"
GADIS_API_SEARCH     = "https://catalog.gadisline.com/api/v3/catalog/products/search"
GADIS_HEADERS = {
    **COMMON_HEADERS,
    "content-type": "application/json",
    "origin": "https://www.gadisline.com",
    "referer": "https://www.gadisline.com/",
    "site-id": "56df88f9-479f-4361-891e-e1864dba1ca3",
    "store-id": "891d5c1e-a7a0-4287-9ea3-30c5703a4f63",
}