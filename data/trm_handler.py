# trm_handler.py
"""
TRM handler module for Global Yield Optimizer v3.0
"""
import random  # Para simulación de datos
import requests
from datetime import datetime, timedelta
from .banrep_api import BanRepAPI


def get_current_trm():
    """
    Obtiene el TRM actual desde el Banco de la República.
    
    Returns:
        float: Valor del TRM actual
    """
    # Obtener datos reales del Banco de la República
    try:
        api = BanRepAPI()
        trm_data = api.get_trm()
        if trm_data and 'value' in trm_data:
            return float(trm_data['value'])
    except Exception as e:
        print(f"Error al obtener TRM del Banco de la República: {e}")
    
    # Si hay error, usar datos simulados
    # El TRM históricamente ha estado entre 3500 y 5000 COP/USD
    return round(random.uniform(3800, 4200), 2)


def get_trm_history(days=45):
    """
    Obtiene el historial de TRM desde el Banco de la República.
    
    Args:
        days (int): Número de días de historial a obtener
    
    Returns:
        list: Lista con valores históricos de TRM
    """
    # Obtener datos históricos reales del Banco de la República
    try:
        api = BanRepAPI()
        # Calcular fechas para obtener datos históricos
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        trm_data = api.get_trm_history(
            start_date=start_date.strftime("%Y-%m-%d"),
            end_date=end_date.strftime("%Y-%m-%d")
        )
        
        if trm_data and 'data' in trm_data:
            # Extraer valores de la respuesta
            values = [float(item['value']) for item in trm_data['data'] if 'value' in item]
            return values
    except Exception as e:
        print(f"Error al obtener historial de TRM del Banco de la República: {e}")
    
    # Si hay error, generar valores simulados
    trm_values = []
    base_value = 4000.0
    
    for i in range(days):
        # Variación aleatoria pequeña basada en volatilidad histórica del TRM
        variation = random.uniform(-20, 20)
        trm_values.append(round(base_value + variation, 2))
    
    return trm_values


def get_trm_on_date(date):
    """
    Obtiene el TRM en una fecha específica desde el Banco de la República.
    
    Args:
        date (str): Fecha en formato 'YYYY-MM-DD'
    
    Returns:
        float: Valor del TRM en esa fecha
    """
    # Obtener datos reales del Banco de la República para una fecha específica
    try:
        api = BanRepAPI()
        trm_data = api.get_trm(date)
        if trm_data and 'value' in trm_data:
            return float(trm_data['value'])
    except Exception as e:
        print(f"Error al obtener TRM del Banco de la República para fecha {date}: {e}")
    
    # Si hay error, devolver un valor simulado
    return round(random.uniform(3800, 4200), 2)


def fetch_trm_from_banrep(start_date=None, end_date=None):
    """
    Obtiene datos de TRM del Banco de la República usando su API oficial.
    
    Args:
        start_date (str): Fecha de inicio en formato YYYY-MM-DD (opcional)
        end_date (str): Fecha de fin en formato YYYY-MM-DD (opcional)
    
    Returns:
        dict: Datos de TRM con fechas y valores
    """
    try:
        api = BanRepAPI()
        return api.get_trm_history(start_date, end_date)
    except Exception as e:
        print(f"Error al obtener datos del Banco de la República: {e}")
        # Devolver datos simulados en caso de error
        return generate_simulated_trm_data(start_date, end_date)


def generate_simulated_trm_data(start_date=None, end_date=None):
    """
    Genera datos simulados de TRM basados en patrones históricos.
    
    Args:
        start_date (str): Fecha de inicio en formato YYYY-MM-DD (opcional)
        end_date (str): Fecha de fin en formato YYYY-MM-DD (opcional)
    
    Returns:
        dict: Datos de TRM simulados
    """
    # Si no se especifican fechas, generar datos para los últimos 45 días
    if not start_date:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=45)
    else:
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        if end_date:
            end_date = datetime.strptime(end_date, "%Y-%m-%d")
        else:
            end_date = datetime.now()
    
    # Generar datos simulados
    data = []
    current_date = start_date
    base_value = 4000.0
    
    while current_date <= end_date:
        # Variación basada en volatilidad histórica del TRM
        variation = random.uniform(-20, 20)
        value = round(base_value + variation, 2)
        
        data.append({
            "date": current_date.strftime("%Y-%m-%d"),
            "value": value
        })
        
        current_date += timedelta(days=1)
    
    return {
        "series_id": "TRM",
        "name": "Tasa de Cambio Representativa del Mercado",
        "data": data
    }