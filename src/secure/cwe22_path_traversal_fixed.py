"""
CWE-22: Path Traversal - Versión Corregida
La vulnerabilidad se corrige validando y normalizando la ruta.
"""

import os

def read_file_secure(filename):
    """
    Lee un archivo del sistema de archivos.
    SEGURO: Valida que la ruta esté dentro del directorio base.
    """
    base_dir = "/var/www/files/"
    
    # CORREGIDO: Normaliza y valida la ruta
    # 1. Obtener la ruta absoluta real
    real_base = os.path.realpath(base_dir)
    real_path = os.path.realpath(os.path.join(base_dir, filename))
    
    # 2. Verificar que la ruta resultante esté dentro del directorio base
    if not real_path.startswith(real_base):
        raise ValueError("Acceso denegado: ruta fuera del directorio permitido")
    
    # 3. Verificar que el archivo existe y es un archivo regular
    if not os.path.isfile(real_path):
        raise FileNotFoundError("El archivo no existe")
    
    with open(real_path, 'r') as f:
        return f.read()