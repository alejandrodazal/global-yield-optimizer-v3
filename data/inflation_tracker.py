# inflation_tracker.py
"""
Inflation tracker module for Global Yield Optimizer v3.0
"""
import random  # Para simulación de datos


def get_current_inflation(country="Colombia"):
    """
    Simula la obtención de la inflación actual de un país.
    En una implementación real, aquí se conectaría a una API oficial.
    
    Args:
        country (str): Nombre del país
    
    Returns:
        float: Tasa de inflación anual
    """
    # Tasas de inflación simuladas para diferentes países
    inflation_rates = {
        "Colombia": round(random.uniform(2.0, 5.0), 2),
        "USA": round(random.uniform(1.0, 4.0), 2),
        "Eurozone": round(random.uniform(1.5, 3.5), 2),
        "Chile": round(random.uniform(2.5, 5.5), 2),
        "Mexico": round(random.uniform(3.0, 6.0), 2)
    }
    
    return inflation_rates.get(country, 3.0)  # Valor por defecto 3.0%


def get_historical_inflation(country="Colombia", months=12):
    """
    Simula la obtención del historial de inflación de un país.
    
    Args:
        country (str): Nombre del país
        months (int): Número de meses de historial
    
    Returns:
        list: Lista con tasas de inflación históricas
    """
    # Generar valores simulados de inflación
    inflation_history = []
    
    for _ in range(months):
        inflation_history.append(round(random.uniform(1.0, 6.0), 2))
    
    return inflation_history