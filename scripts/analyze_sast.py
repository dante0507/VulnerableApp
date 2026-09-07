"""
analyze_sast.py - Módulo de análisis SAST
Este script ejecuta herramientas de análisis estático sobre el código generado.
"""

import os
import json
import subprocess

def run_bandit(code_path):
    """
    Ejecuta Bandit sobre el código.
    
    Args:
        code_path: Ruta al archivo o directorio a analizar
    
    Returns:
        dict: Resultados del análisis en formato JSON
    """
    
    result = subprocess.run(
        ['bandit', '-r', '-f', 'json', code_path],
        capture_output=True,
        text=True
    )
    
    return json.loads(result.stdout)

def run_codeql(code_path):
    """
    Ejecuta CodeQL sobre el código.
    
    Args:
        code_path: Ruta al archivo o directorio a analizar
    
    Returns:
        dict: Resultados del análisis en formato SARIF
    """
    
    # Crear base de datos
    subprocess.run([
        'codeql', 'database', 'create', './db',
        '--language=python',
        f'--source-root={code_path}'
    ])
    
    # Ejecutar análisis
    result = subprocess.run([
        'codeql', 'database', 'analyze', './db',
        'codeql/python-queries:codeql-suites/python-security-extended.qls',
        '--format=sarif-latest',
        '--output=results.sarif'
    ])
    
    with open('results.sarif', 'r') as f:
        return json.load(f)

def run_sonarqube(project_path):
    """
    Ejecuta SonarQube sobre el proyecto.
    
    Args:
        project_path: Ruta al proyecto a analizar
    """
    
    subprocess.run([
        'sonar-scanner',
        f'-Dsonar.projectKey=VulnerableApp',
        f'-Dsonar.sources={project_path}'
    ])

def main():
    """
    Función principal: analiza todo el código generado.
    """
    
    # Analizar archivos vulnerables
    print("Ejecutando Bandit...")
    bandit_results = run_bandit("src/vulnerable/")
    with open("results/resultados_bandit.json", "w") as f:
        json.dump(bandit_results, f, indent=2)
    print("Resultados guardados en results/resultados_bandit.json")
    
    print("Ejecutando CodeQL...")
    run_codeql("src/")
    print("Resultados guardados en results/resultados_codeql.sarif")
    
    print("Ejecutando SonarQube...")
    run_sonarqube(".")
    print("Análisis de SonarQube completado.")

if __name__ == "__main__":
    main()