"""
generate.py - Módulo de generación de código con LLMs
Este script genera código utilizando diferentes modelos de lenguaje.
"""

import os
import json
import time
from openai import OpenAI
import yaml

# Cargar configuración
with open('config/models.yaml', 'r') as f:
    models_config = yaml.safe_load(f)

with open('config/languages.yaml', 'r') as f:
    languages_config = yaml.safe_load(f)

def generate_code(model_name, language, task_description, temperature=0.9):
    """
    Genera código utilizando el modelo especificado.
    
    Args:
        model_name: Nombre del modelo (GPT-4o, Claude, Gemini, etc.)
        language: Lenguaje de programación (Python, Java, C++, C)
        task_description: Descripción de la tarea a resolver
        temperature: Parámetro de temperatura (0.0 - 1.0)
    
    Returns:
        str: Código generado
    """
    
    # Construir el prompt
    prompt = f"""
Write a complete {language} program to solve the following problem:
{task_description}

The program must be compilable/executable and functionally correct.
"""
    
    # Llamar a la API correspondiente según el modelo
    if model_name == "GPT-4o":
        client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature
        )
        return response.choices[0].message.content
    
    # Añadir aquí llamadas para Claude, Gemini, Codestral, Llama-3
    # ...
    
    return ""

def main():
    """
    Función principal: genera código para todas las combinaciones
    modelo × lenguaje × tarea.
    """
    
    # Cargar tareas
    with open('config/tasks.json', 'r') as f:
        tasks = json.load(f)
    
    # Para cada combinación, generar código
    for model in models_config['models']:
        for language in languages_config['languages']:
            for task in tasks:
                print(f"Generando: {model['name']} - {language} - {task['id']}")
                
                code = generate_code(
                    model_name=model['name'],
                    language=language,
                    task_description=task['description']
                )
                
                # Guardar el código generado
                output_dir = f"generated/{model['name']}/{language}"
                os.makedirs(output_dir, exist_ok=True)
                filename = f"{output_dir}/{task['id']}_1.{language.lower()}"
                
                with open(filename, 'w') as f:
                    f.write(code)

if __name__ == "__main__":
    main()