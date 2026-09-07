"""
CWE-89: SQL Injection - Versión Corregida
La vulnerabilidad se corrige utilizando consultas parametrizadas.
"""

import sqlite3

def get_user_secure(username):
    """
    Obtiene un usuario de la base de datos por su nombre de usuario.
    SEGURO: Usa consultas parametrizadas.
    """
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    #CORREGIDO: Uso de consulta parametrizada
    query = "SELECT * FROM users WHERE username = ?"
    cursor.execute(query, (username,))
    
    result = cursor.fetchone()
    conn.close()
    return result