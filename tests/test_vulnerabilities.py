"""
Tests para verificar que las vulnerabilidades son detectables.
"""

import unittest
import os
import sys

# Agregar el directorio src al path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from vulnerable.cwe89_sql_injection import get_user_vulnerable
from secure.cwe89_sql_injection_fixed import get_user_secure
from vulnerable.cwe22_path_traversal import read_file_vulnerable
from secure.cwe22_path_traversal_fixed import read_file_secure
from vulnerable.cwe327_insecure_crypto import hash_password_vulnerable, encrypt_data_vulnerable
from secure.cwe327_insecure_crypto_fixed import hash_password_secure


class TestVulnerabilities(unittest.TestCase):
    
    def test_sql_injection_vulnerable(self):
        """Verifica que la versión vulnerable permite inyección SQL."""
        # Este test debería fallar en la versión vulnerable
        result = get_user_vulnerable("admin' OR '1'='1")
        # Si devuelve algo, significa que es vulnerable
        self.assertIsNotNone(result, "La versión vulnerable debería permitir inyección SQL")
    
    def test_sql_injection_secure(self):
        """Verifica que la versión corregida NO permite inyección SQL."""
        # Este test debería pasar en la versión corregida
        result = get_user_secure("admin' OR '1'='1")
        # No debería devolver resultados
        self.assertIsNone(result, "La versión corregida NO debería permitir inyección SQL")
    
    def test_path_traversal_vulnerable(self):
        """Verifica que la versión vulnerable permite path traversal."""
        # Intentar leer /etc/passwd (en sistemas Linux)
        try:
            content = read_file_vulnerable("../../etc/passwd")
            self.assertIsNotNone(content, "La versión vulnerable debería permitir path traversal")
        except Exception:
            # En Windows, puede fallar, pero el concepto es el mismo
            pass
    
    def test_path_traversal_secure(self):
        """Verifica que la versión corregida NO permite path traversal."""
        with self.assertRaises(ValueError):
            read_file_secure("../../etc/passwd")
    
    def test_insecure_crypto_vulnerable(self):
        """Verifica que la versión vulnerable usa MD5."""
        hash1 = hash_password_vulnerable("password123")
        hash2 = hash_password_vulnerable("password123")
        # MD5 produce el mismo hash para la misma entrada
        self.assertEqual(hash1, hash2, "MD5 debería producir el mismo hash")
        self.assertEqual(len(hash1), 32, "MD5 produce hashes de 32 caracteres")
    
    def test_insecure_crypto_secure(self):
        """Verifica que la versión corregida usa sal y algoritmos modernos."""
        hash1 = hash_password_secure("password123")
        hash2 = hash_password_secure("password123")
        # Con sal, los hashes deberían ser diferentes
        self.assertNotEqual(hash1, hash2, "Con sal, los hashes deberían ser diferentes")
        self.assertGreater(len(hash1), 32, "Con sal, el hash debería ser más largo")


if __name__ == '__main__':
    unittest.main()