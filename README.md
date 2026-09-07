# VulnerableApp - Dataset para pruebas de seguridad

Este proyecto contiene ejemplos de código con vulnerabilidades comunes (CWE) para probar herramientas de análisis estático de seguridad (SAST).

## Vulnerabilidades incluidas

- **CWE-89**: SQL Injection
- **CWE-79**: Cross-Site Scripting (XSS)
- **CWE-22**: Path Traversal
- **CWE-327**: Insecure Cryptography

## Estructura

- `src/vulnerable/`: Código con vulnerabilidades
- `src/secure/`: Código corregido
- `tests/`: Tests unitarios

## Instalación

```bash
pip install -r requirements.txt