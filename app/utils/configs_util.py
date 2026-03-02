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

# --- EROSKI ---
EROSKI_BASE_CAT_URL = "https://supermercado.eroski.es/es/supermercado/2059806-alimentacion/{cat}/p-{page}/"

EROSKI_COOKIES = {
    "p_provincia": "15",
    "p_tienda": "00155",
    "s_language": "es"
}

EROSKI_HEADERS = {
    "accept": "*/*",
    "accept-language": "es-ES,es;q=0.9",
    "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
    "origin": "https://supermercado.eroski.es",
    "x-requested-with": "XMLHttpRequest",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
}