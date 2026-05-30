# --- COMMON ---
COMMON_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/120.0.0.0',
    'Accept-Language': 'es-ES,es;q=0.9',
    'Connection': 'keep-alive',
}

# --- MERCADONA (WH=4592) ---
MERCADONA_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/120.0.0.0',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'es-ES,es;q=0.9',
    'Referer': "https://tienda.mercadona.es/",
    'Origin': "https://tienda.mercadona.es",
    'Connection': 'keep-alive'
}
MERCADONA_API_INDEX = "https://tienda.mercadona.es/api/categories/?lang=es&wh=4592"
MERCADONA_API_CAT   = "https://tienda.mercadona.es/api/categories/{cat_id}/?lang=es&wh=4592"

# --- EROSKI ---
EROSKI_BASE_URL = "https://supermercado.eroski.es/es/supermercado/2059806-alimentacion/"
EROSKI_AJAX_URL = "https://supermercado.eroski.es/es/supermarket.productfiltermenu:globalfilter"
EROSKI_HEADERS = {
    **COMMON_HEADERS,
    "X-Requested-With": "XMLHttpRequest",
    "X-Tapestry-Ajax": "true",
    "Origin": "https://supermercado.eroski.es",
    "Referer": EROSKI_BASE_URL,
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
}

# --- GADIS ---
GADIS_API_SEARCH = "https://catalog.gadisline.com/api/v3/catalog/products/search"
GADIS_HEADERS = {
    **COMMON_HEADERS,
    "accept": "application/json",
    "content-type": "application/json",
    "origin": "https://www.gadisline.com",
    "referer": "https://www.gadisline.com/",
    "site-id": "56df88f9-479f-4361-891e-e1864dba1ca3",
    "store-id": "891d5c1e-a7a0-4287-9ea3-30c5703a4f63",
    "time-zone": "Europe/Madrid",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
}
GADIS_CATEGORIES = ["8a98965c-e5d7-44b2-9b22-1f9a6521d916"]