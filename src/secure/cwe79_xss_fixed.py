"""
CWE-79: Cross-Site Scripting (XSS) - Versión Corregida
La vulnerabilidad se corrige escapando la salida HTML.
"""

from flask import Flask, request, render_template_string, escape

app = Flask(__name__)

@app.route('/xss_secure')
def xss_secure():
    """
    Endpoint seguro porque escapa el input del usuario antes de mostrarlo.
    """
    user_input = request.args.get('q', '')
    
    # CORREGIDO: Escapa la salida HTML
    safe_input = escape(user_input)
    
    template = """
    <html>
        <body>
            <h1>Resultados de búsqueda</h1>
            <p>Has buscado: """ + safe_input + """</p>
        </body>
    </html>
    """
    return render_template_string(template)