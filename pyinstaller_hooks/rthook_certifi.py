import os
import sys
import ssl
from app.utils.logger_util import HermesLogger

def _patch_ssl():
    log = HermesLogger.get_logger("SSL_PATCH")
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
        cert_path = os.path.join(base_path, 'certifi', 'cacert.pem')
        
        os.environ['REQUESTS_CA_BUNDLE'] = cert_path
        os.environ['SSL_CERT_FILE'] = cert_path

        try:
            import certifi
            certifi.where = lambda: cert_path
            
            import requests.utils
            import requests.adapters
            requests.utils.DEFAULT_CA_BUNDLE_PATH = cert_path
            requests.adapters.DEFAULT_CA_BUNDLE_PATH = cert_path
            
            import urllib3.util.ssl_
            urllib3.util.ssl_.DEFAULT_CA_BUNDLE_PATH = cert_path
            
            with open(cert_path, 'r', encoding='utf-8') as f:
                cert_data = f.read()
            ctx = ssl.create_default_context()
            ctx.load_verify_locations(cadata=cert_data)
            
            def patched_verify(self, conn, url, verify, cert):
                conn.ca_certs = cert_path
                conn.verify_mode = ssl.CERT_REQUIRED
                return 

            requests.adapters.HTTPAdapter.cert_verify = patched_verify
            log.info("Parche SSL aplicado correctamente en entorno frozen.")
        except Exception as e:
            log.error(f"Error aplicando parche SSL: {e}")

_patch_ssl()