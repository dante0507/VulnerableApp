"""
CWE-89: SQL Injection - Versión Vulnerable
Esta función es vulnerable porque concatena directamente la entrada del usuario
en la consulta SQL sin sanitización ni parametrización.
"""

import sqlite3

def get_user_vulnerable(username):
    """
    Obtiene un usuario de la base de datos por su nombre de usuario.
    VULNERABLE a SQL Injection.
    """
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # VULNERABLE: Concatenación directa de input del usuario
    query = "SELECT * FROM users WHERE username = '" + username + "'"
    cursor.execute(query)
    
    result = cursor.fetchone()
    conn.close()
    return result

# Ejemplo de exploit: username = "admin' OR '1'='1"
# Esto devolvería TODOS los usuarios de la base de datos