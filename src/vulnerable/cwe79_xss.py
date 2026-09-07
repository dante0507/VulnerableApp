"""
CWE-79: Cross-Site Scripting (XSS) - Versión Vulnerable
Esta función es vulnerable porque devuelve directamente el input del usuario
sin sanitización, permitiendo inyección de scripts maliciosos.
"""

from flask import Flask, request, render_template_string

app = Flask(__name__)

@app.route('/xss_vulnerable')
def xss_vulnerable():
    """
    Endpoint vulnerable a XSS porque muestra el input del usuario sin escapar.
    """
    user_input = request.args.get('q', '')
    
    # VULNERABLE: Renderiza el input directamente sin sanitizar
    template = """
    <html>
        <body>
            <h1>Resultados de búsqueda</h1>
            <p>Has buscado: """ + user_input + """</p>
        </body>
    </html>
    """
    return render_template_string(template)

# Ejemplo de exploit: /xss_vulnerable?q=<script>alert('XSS')</script>