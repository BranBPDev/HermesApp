import os
import sys
import ssl
import importlib

if getattr(sys, 'frozen', False):
    # 1. Localizar el certificado real extraído
    base_path = sys._MEIPASS
    cert_path = os.path.join(base_path, 'certifi', 'cacert.pem')
    
    print(f"\n[DEBUG-SYS] MEIPASS: {base_path}")
    print(f"[DEBUG-SYS] Cert existe en disco: {os.path.exists(cert_path)}")

    # 2. Forzar variables de entorno ANTES de que requests respire
    os.environ['REQUESTS_CA_BUNDLE'] = cert_path
    os.environ['SSL_CERT_FILE'] = cert_path

    try:
        # 3. Parchear los módulos aunque ya estén cargados
        import certifi
        certifi.where = lambda: cert_path
        
        import requests.utils
        import requests.adapters
        
        # Forzamos la ruta en el lugar donde requests la busca internamente
        requests.utils.DEFAULT_CA_BUNDLE_PATH = cert_path
        requests.adapters.DEFAULT_CA_BUNDLE_PATH = cert_path
        
        # 4. Parchear urllib3 (el motor real)
        import urllib3.util.ssl_
        urllib3.util.ssl_.DEFAULT_CA_BUNDLE_PATH = cert_path
        
        # 5. Inyectar el contexto de memoria como último recurso
        with open(cert_path, 'r', encoding='utf-8') as f:
            cert_data = f.read()
        ctx = ssl.create_default_context()
        ctx.load_verify_locations(cadata=cert_data)
        
        # Sobrescribimos la verificación de Requests para que NO mire el disco
        def patched_verify(self, conn, url, verify, cert):
            conn.ca_certs = cert_path
            conn.verify_mode = ssl.CERT_REQUIRED
            return # Saltamos el chequeo de os.path.exists()

        requests.adapters.HTTPAdapter.cert_verify = patched_verify
        
        print("[DEBUG-OK] Parche integral aplicado (Entorno + RAM + Adaptador)")
    except Exception as e:
        print(f"[DEBUG-ERR] Error aplicando parches: {e}")