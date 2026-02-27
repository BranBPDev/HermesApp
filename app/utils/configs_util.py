COMMON_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    'Accept': 'application/json',
}

# MERCADONA
MERCADONA_API_INDEX = "https://tienda.mercadona.es/api/categories/?lang=es&wh=4592"
MERCADONA_API_CAT   = "https://tienda.mercadona.es/api/categories/{cat_id}/?lang=es&wh=4592"

# LIDL (Cambiamos a la de búsqueda que es más estable)
LIDL_API_SEARCH = "https://www.lidl.es/es/api/search/search?query=*&pageSize=500"

# GADIS
GADIS_API_CATEGORIES = "https://catalog.gadisline.com/api/v3/catalog/categories"
GADIS_API_SEARCH     = "https://catalog.gadisline.com/api/v3/catalog/products/search"
GADIS_HEADERS = {
    "accept": "application/json, text/plain, */*",
    "content-type": "application/json",
    "origin": "https://www.gadisline.com",
    "referer": "https://www.gadisline.com/",
    "site-id": "56df88f9-479f-4361-891e-e1864dba1ca3",
    "store-id": "891d5c1e-a7a0-4287-9ea3-30c5703a4f63",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
}

# EROSKI (Su API de búsqueda es rápida)
EROSKI_API_SEARCH = "https://www.compraonline.eroski.es/es/api/v1/search/products?q=*&filter=categories%3A1"