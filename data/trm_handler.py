# trm_handler.py
"""
TRM handler module for Global Yield Optimizer v3.0
"""
import random  # Para simulación de datos
from datetime import datetime, timedelta


def get_current_trm():
    """
    Simula la obtención del TRM actual.
    En una implementación real, aquí se conectaría a una API oficial.
    
    Returns:
        float: Valor del TRM actual
    """
    # Simular un valor de TRM actual
    return round(random.uniform(3800, 4200), 2)


def get_trm_history(days=45):
    """
    Simula la obtención del historial de TRM.
    
    Args:
        days (int): Número de días de historial a obtener
    
    Returns:
        list: Lista con valores históricos de TRM
    """
    # Generar valores simulados de TRM para los últimos 'days' días
    trm_values = []
    base_value = 4000.0
    
    for i in range(days):
        # Variación aleatoria pequeña
        variation = random.uniform(-10, 10)
        trm_values.append(base_value + variation)
    
    return trm_values


def get_trm_on_date(date):
    """
    Simula la obtención del TRM en una fecha específica.
    
    Args:
        date (str): Fecha en formato 'YYYY-MM-DD'
    
    Returns:
        float: Valor del TRM en esa fecha
    """
    # En una implementación real, buscaría en la base de datos
    # Aquí simplemente devolvemos un valor simulado
    return round(random.uniform(3800, 4200), 2)