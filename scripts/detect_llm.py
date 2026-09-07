"""
detect_llm.py - Módulo de detección de vulnerabilidades con LLMs
Este script utiliza los LLMs para detectar vulnerabilidades en código.
"""

import os
import json
from openai import OpenAI
import yaml

# Cargar configuración
with open('config/prompts/detection_prompt.txt', 'r') as f:
    DETECTION_PROMPT_TEMPLATE = f.read()

def detect_vulnerabilities_llm(model_name, code, cwe_id=None):
    """
    Detecta vulnerabilidades en el código utilizando un LLM.
    
    Args:
        model_name: Nombre del modelo a utilizar
        code: Código a analizar
        cwe_id: CWE específico a buscar (opcional)
    
    Returns:
        dict: Vulnerabilidades detectadas en formato JSON
    """
    
    # Construir el prompt específico
    if cwe_id:
        prompt = DETECTION_PROMPT_TEMPLATE.replace(
            "{CWE_SPECIFIC}",
            f"Busca específicamente vulnerabilidades de tipo {cwe_id}."
        )
    else:
        prompt = DETECTION_PROMPT_TEMPLATE.replace(
            "{CWE_SPECIFIC}",
            "Busca cualquier tipo de vulnerabilidad."
        )
    
    prompt = prompt.replace("{CODE}", code)
    
    # Llamar a la API
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": "Devuelve siempre un JSON válido."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.0
    )
    
    return json.loads(response.choices[0].message.content)

def main():
    """
    Función principal: ejecuta la detección sobre los archivos de prueba.
    """
    
    models = ["gpt-4o", "claude-3-5-sonnet", "gemini-1.5-pro"]
    
    # Archivos a analizar
    files = [
        "src/vulnerable/cwe89_sql_injection.py",
        "src/secure/cwe89_sql_injection_fixed.py",
        "src/vulnerable/cwe79_xss.py",
        "src/secure/cwe79_xss_fixed.py"
    ]
    
    results = {}
    
    for model in models:
        print(f"\n=== Analizando con {model} ===")
        results[model] = {}
        
        for file_path in files:
            print(f"  Analizando: {file_path}")
            
            with open(file_path, 'r') as f:
                code = f.read()
            
            # Detectar vulnerabilidades
            try:
                detection_result = detect_vulnerabilities_llm(
                    model_name=model,
                    code=code
                )
                results[model][file_path] = detection_result
            except Exception as e:
                print(f"    Error: {e}")
                results[model][file_path] = {"error": str(e)}
    
    # Guardar resultados
    with open("results/resultados_deteccion_llm.json", "w") as f:
        json.dump(results, f, indent=2)
    print("\nResultados guardados en results/resultados_deteccion_llm.json")

if __name__ == "__main__":
    main()