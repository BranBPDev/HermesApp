import bcrypt
import base64

def hash_password(password: str) -> str:
    """Genera un hash seguro para la base de datos."""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def check_password(password: str, hashed: str) -> bool:
    """Valida una contraseña contra su hash."""
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def encode_to_base64(text: str) -> str:
    """Ofusca texto para almacenamiento local rápido."""
    return base64.b64encode(text.encode('utf-8')).decode('utf-8')

def decode_from_base64(encoded_text: str) -> str:
    """Desofusca texto almacenado localmente."""
    return base64.b64decode(encoded_text.encode('utf-8')).decode('utf-8')