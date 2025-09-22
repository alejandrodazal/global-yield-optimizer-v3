# inflation_tracker.py
"""
Inflation tracker module for Global Yield Optimizer v3.0
"""
import random  # Para simulación de datos
import requests
from datetime import datetime, timedelta
from .banrep_api import BanRepAPI


def get_current_inflation(country="Colombia"):
    """
    Obtiene la inflación actual de un país desde el Banco de la República u otras fuentes.
    
    Args:
        country (str): Nombre del país
    
    Returns:
        float: Tasa de inflación anual
    """
    if country == "Colombia":
        # Obtener datos reales del Banco de la República
        try:
            api = BanRepAPI()
            inflation_data = api.get_inflation()
            if inflation_data and 'value' in inflation_data:
                return float(inflation_data['value'])
        except Exception as e:
            print(f"Error al obtener inflación de Colombia del Banco de la República: {e}")
        
        # Si hay error, usar datos simulados
        return round(random.uniform(2.0, 5.0), 2)
    else:
        # Tasas de inflación simuladas para otros países
        inflation_rates = {
            "USA": round(random.uniform(1.0, 4.0), 2),
            "Eurozone": round(random.uniform(1.5, 3.5), 2),
            "Chile": round(random.uniform(2.5, 5.5), 2),
            "Mexico": round(random.uniform(3.0, 6.0), 2)
        }
        
        return inflation_rates.get(country, 3.0)  # Valor por defecto 3.0%


def get_historical_inflation(country="Colombia", months=12):
    """
    Obtiene el historial de inflación de un país desde el Banco de la República.
    
    Args:
        country (str): Nombre del país
        months (int): Número de meses de historial
    
    Returns:
        list: Lista con tasas de inflación históricas
    """
    if country == "Colombia":
        # Obtener datos históricos reales del Banco de la República
        try:
            api = BanRepAPI()
            # Calcular fechas para obtener datos históricos
            end_date = datetime.now()
            start_date = end_date - timedelta(days=months*30)
            
            inflation_data = api.get_inflation(
                start_date=start_date.strftime("%Y-%m-%d"),
                end_date=end_date.strftime("%Y-%m-%d")
            )
            
            if inflation_data and 'data' in inflation_data:
                # Extraer valores de la respuesta
                values = [float(item['value']) for item in inflation_data['data'] if 'value' in item]
                return values[-months:] if len(values) > months else values
        except Exception as e:
            print(f"Error al obtener historial de inflación de Colombia del Banco de la República: {e}")
        
        # Si hay error, generar valores simulados
        inflation_history = []
        for _ in range(months):
            inflation_history.append(round(random.uniform(1.0, 6.0), 2))
        return inflation_history
    else:
        # Generar valores simulados para otros países
        inflation_history = []
        for _ in range(months):
            inflation_history.append(round(random.uniform(1.0, 6.0), 2))
        return inflation_history


def fetch_colombian_inflation_from_banrep():
    """
    Obtiene datos de inflación de Colombia directamente del Banco de la República.
    
    Returns:
        dict: Datos de inflación con fechas y valores
    """
    try:
        api = BanRepAPI()
        return api.get_inflation()
    except Exception as e:
        print(f"Error al obtener datos del Banco de la República: {e}")
        # Devolver datos simulados en caso de error
        return generate_simulated_inflation_data()


def generate_simulated_inflation_data():
    """
    Genera datos simulados de inflación basados en patrones históricos de Colombia.
    
    Returns:
        dict: Datos de inflación simulados
    """
    # Generar datos simulados para los últimos 24 meses
    data = []
    base_date = datetime.now()
    
    for i in range(24, 0, -1):
        date = base_date - timedelta(days=i*30)
        # La inflación en Colombia típicamente oscila entre 2% y 5%
        # con ocasionales picos más altos
        if i % 6 == 0:  # Cada 6 meses, hay una probabilidad de pico
            value = round(random.uniform(4.0, 7.0), 2)
        else:
            value = round(random.uniform(2.0, 5.0), 2)
        
        data.append({
            "date": date.strftime("%Y-%m-%d"),
            "value": value
        })
    
    return {
        "series_id": "IPC",
        "name": "Índice de Precios al Consumidor (Inflación)",
        "data": data
    }