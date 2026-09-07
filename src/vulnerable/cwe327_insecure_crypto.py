"""
CWE-327: Use of a Broken or Risky Cryptographic Algorithm - Versión Vulnerable
Esta función usa algoritmos criptográficos obsoletos e inseguros.
"""

import hashlib
from Crypto.Cipher import DES

def hash_password_vulnerable(password):
    """
    Hashea una contraseña usando MD5.
    VULNERABLE: MD5 es considerado inseguro para contraseñas.
    """
    # VULNERABLE: MD5 es un algoritmo débil y roto
    return hashlib.md5(password.encode()).hexdigest()

def encrypt_data_vulnerable(data, key):
    """
    Cifra datos usando DES.
    VULNERABLE: DES es considerado obsoleto y fácil de romper.
    """
    # VULNERABLE: DES tiene un tamaño de clave de 56 bits (débil)
    cipher = DES.new(key[:8].encode(), DES.MODE_ECB)
    return cipher.encrypt(data.encode())

# Ejemplo: Un atacante puede romper el hash MD5 en milisegundos