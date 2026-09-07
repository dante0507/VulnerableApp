"""
CWE-22: Path Traversal - Versión Vulnerable
Esta función es vulnerable porque permite acceder a archivos fuera del directorio
base mediante caracteres como "../".
"""

import os

def read_file_vulnerable(filename):
    """
    Lee un archivo del sistema de archivos.
    VULNERABLE a Path Traversal.
    """
    base_dir = "/var/www/files/"
    
    # VULNERABLE: Concatena directamente el input del usuario
    filepath = base_dir + filename
    
    with open(filepath, 'r') as f:
        return f.read()

# Ejemplo de exploit: filename = "../../etc/passwd"
# Esto leería el archivo de contraseñas del sistema