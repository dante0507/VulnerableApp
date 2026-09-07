"""
CWE-327: Use of a Broken or Risky Cryptographic Algorithm - Versión Corregida
Se utilizan algoritmos modernos y seguros.
"""

import hashlib
import secrets
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

def hash_password_secure(password):
    """
    Hashea una contraseña usando un algoritmo moderno.
    SEGURO: Usa PBKDF2 con sal.
    """
    # CORREGIDO: Usar sal y algoritmo fuerte
    salt = secrets.token_bytes(16)
    key = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
    return salt.hex() + key.hex()

def encrypt_data_secure(data, password):
    """
    Cifra datos usando un algoritmo moderno.
    SEGURO: Usa Fernet (AES-128 en modo CBC con autenticación).
    """
    # CORREGIDO: Usar Fernet (AES-128 en modo CBC)
    # 1. Derivar una clave a partir de la contraseña
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=b'salt_',
        iterations=100000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    
    # 2. Cifrar con Fernet
    f = Fernet(key)
    return f.encrypt(data.encode()).decode()