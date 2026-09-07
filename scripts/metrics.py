"""
metrics.py - Módulo de cálculo de métricas
Este script calcula las métricas de evaluación (precisión, recall, F1, etc.)
"""

import json
import math

def calculate_confusion_matrix(ground_truth, predictions):
    """
    Calcula la matriz de confusión.
    
    Args:
        ground_truth: Lista de valores reales (True/False)
        predictions: Lista de predicciones (True/False)
    
    Returns:
        dict: TP, TN, FP, FN
    """
    
    TP = sum(1 for gt, pred in zip(ground_truth, predictions) if gt and pred)
    TN = sum(1 for gt, pred in zip(ground_truth, predictions) if not gt and not pred)
    FP = sum(1 for gt, pred in zip(ground_truth, predictions) if not gt and pred)
    FN = sum(1 for gt, pred in zip(ground_truth, predictions) if gt and not pred)
    
    return {"TP": TP, "TN": TN, "FP": FP, "FN": FN}

def calculate_metrics(TP, TN, FP, FN):
    """
    Calcula precisión, recall y F1-score.
    
    Args:
        TP, TN, FP, FN: Valores de la matriz de confusión
    
    Returns:
        dict: Precisión, Recall, F1-score
    """
    
    precision = TP / (TP + FP) if (TP + FP) > 0 else 0
    recall = TP / (TP + FN) if (TP + FN) > 0 else 0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    
    return {
        "precision": precision,
        "recall": recall,
        "f1_score": f1
    }

def calculate_castle_score(TP, FP, cwe_rank=0):
    """
    Calcula el CASTLE Score adaptado.
    
    Args:
        TP: Verdaderos positivos
        FP: Falsos positivos
        cwe_rank: Ranking del CWE (1-25, 0 si no está en Top 25)
    
    Returns:
        float: CASTLE Score
    """
    
    # Bonus por CWE (0-5 puntos)
    if cwe_rank == 0:
        bonus = 0
    elif cwe_rank <= 5:
        bonus = 5
    elif cwe_rank <= 10:
        bonus = 4
    elif cwe_rank <= 15:
        bonus = 3
    elif cwe_rank <= 20:
        bonus = 2
    else:
        bonus = 1
    
    # Puntuación base: 5 puntos por TP, menos 1 por cada FP
    score = (TP * 5) - FP + (TP * bonus)
    
    return score

def main():
    """
    Función principal: calcula todas las métricas.
    """
    
    # Ejemplo: resultados de Bandit
    # Supongamos que Bandit detectó 3 de 4 vulnerabilidades y 0 FP
    TP = 3
    TN = 0
    FP = 0
    FN = 1
    
    metrics = calculate_metrics(TP, TN, FP, FN)
    castle = calculate_castle_score(TP, FP, 0)
    
    print(f"=== Métricas de Bandit ===")
    print(f"TP: {TP}, TN: {TN}, FP: {FP}, FN: {FN}")
    print(f"Precisión: {metrics['precision']:.2%}")
    print(f"Recall: {metrics['recall']:.2%}")
    print(f"F1-score: {metrics['f1_score']:.2%}")
    print(f"CASTLE Score: {castle}")

if __name__ == "__main__":
    main()