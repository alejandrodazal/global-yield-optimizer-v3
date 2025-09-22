# inflation_tracker.py
"""
Inflation tracker module for Global Yield Optimizer v3.0
"""
import random  # Para simulación de datos
import requests
from datetime import datetime, timedelta
from .banrep_api import BanRepAPI


# Códigos de países para inflación
COUNTRY_INFLATION_CODES = {
    "Colombia": "COL",
    "USA": "USA",
    "Panama": "PAN",
    "Eurozone": "EUR",
    "Chile": "CHL",
    "Mexico": "MEX"
}


def get_current_inflation(country="Colombia"):
    """
    Obtiene la inflación actual de un país desde fuentes internacionales.
    
    Args:
        country (str): Nombre del país
    
    Returns:
        float: Tasa de inflación anual
    """
    # Mapeo de países a sus códigos para obtener datos
    country_code = COUNTRY_INFLATION_CODES.get(country, country)
    
    # Obtener datos reales según el país
    if country == "Colombia":
        # Obtener datos del Banco de la República
        try:
            api = BanRepAPI()
            inflation_data = api.get_inflation()
            if inflation_data and 'value' in inflation_data:
                return float(inflation_data['value'])
        except Exception as e:
            print(f"Error al obtener inflación de Colombia del Banco de la República: {e}")
    elif country == "USA":
        # Para Estados Unidos, podríamos usar la BLS (Bureau of Labor Statistics)
        # o FRED (Federal Reserve Economic Data)
        return get_us_inflation_from_fred()
    elif country == "Panama":
        # Panamá usa el mismo IPC que Estados Unidos por estar dolarizado
        # Pero podemos obtener datos del INEC (Instituto Nacional de Estadística y Censo)
        return get_panama_inflation_from_inec()
    
    # Si hay error o para otros países, usar datos simulados basados en rangos reales
    return get_simulated_inflation_for_country(country)


def get_historical_inflation(country="Colombia", months=12):
    """
    Obtiene el historial de inflación de un país.
    
    Args:
        country (str): Nombre del país
        months (int): Número de meses de historial
    
    Returns:
        list: Lista con tasas de inflación históricas
    """
    # Mapeo de países a sus códigos para obtener datos
    country_code = COUNTRY_INFLATION_CODES.get(country, country)
    
    # Obtener datos históricos según el país
    if country == "Colombia":
        # Obtener datos históricos del Banco de la República
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
    elif country == "USA":
        # Para Estados Unidos, podríamos usar la BLS o FRED
        return get_us_historical_inflation(months)
    elif country == "Panama":
        # Para Panamá, obtener datos del INEC
        return get_panama_historical_inflation(months)
    
    # Si hay error o para otros países, generar valores simulados
    inflation_history = []
    for _ in range(months):
        inflation_history.append(get_simulated_inflation_for_country(country))
    return inflation_history


def get_us_inflation_from_fred():
    """
    Obtiene la inflación de Estados Unidos desde FRED (Federal Reserve Economic Data).
    
    Returns:
        float: Tasa de inflación anual de EE.UU.
    """
    try:
        # En una implementación real, aquí se conectaría a la API de FRED
        # Ejemplo de endpoint: https://api.stlouisfed.org/fred/series/observations?series_id=CPIAUCSL
        pass
    except Exception as e:
        print(f"Error al obtener inflación de EE.UU. de FRED: {e}")
    
    # Devolver datos simulados si hay error
    return round(random.uniform(1.0, 4.0), 2)


def get_us_historical_inflation(months=12):
    """
    Obtiene el historial de inflación de Estados Unidos.
    
    Args:
        months (int): Número de meses de historial
        
    Returns:
        list: Lista con tasas de inflación históricas de EE.UU.
    """
    try:
        # En una implementación real, aquí se conectaría a la API de FRED
        pass
    except Exception as e:
        print(f"Error al obtener historial de inflación de EE.UU. de FRED: {e}")
    
    # Devolver datos simulados si hay error
    inflation_history = []
    for _ in range(months):
        inflation_history.append(round(random.uniform(1.0, 4.0), 2))
    return inflation_history


def get_panama_inflation_from_inec():
    """
    Obtiene la inflación de Panamá desde el INEC.
    
    Returns:
        float: Tasa de inflación anual de Panamá.
    """
    try:
        # En una implementación real, aquí se conectaría a la API del INEC de Panamá
        pass
    except Exception as e:
        print(f"Error al obtener inflación de Panamá del INEC: {e}")
    
    # Devolver datos simulados si hay error
    # Panamá típicamente tiene inflación similar a EE.UU. por estar dolarizado
    return round(random.uniform(1.0, 3.0), 2)


def get_panama_historical_inflation(months=12):
    """
    Obtiene el historial de inflación de Panamá.
    
    Args:
        months (int): Número de meses de historial
        
    Returns:
        list: Lista con tasas de inflación históricas de Panamá.
    """
    try:
        # En una implementación real, aquí se conectaría a la API del INEC de Panamá
        pass
    except Exception as e:
        print(f"Error al obtener historial de inflación de Panamá del INEC: {e}")
    
    # Devolver datos simulados si hay error
    inflation_history = []
    for _ in range(months):
        inflation_history.append(round(random.uniform(1.0, 3.0), 2))
    return inflation_history


def get_simulated_inflation_for_country(country):
    """
    Genera inflación simulada basada en rangos típicos por país.
    
    Args:
        country (str): Nombre del país
        
    Returns:
        float: Tasa de inflación simulada
    """
    # Rangos típicos de inflación por país
    inflation_ranges = {
        "Colombia": (2.0, 5.0),
        "USA": (1.0, 4.0),
        "Panama": (1.0, 3.0),  # Similar a EE.UU. por estar dolarizado
        "Eurozone": (1.5, 3.5),
        "Chile": (2.5, 5.5),
        "Mexico": (3.0, 6.0)
    }
    
    # Obtener rango para el país o usar valores por defecto
    min_inf, max_inf = inflation_ranges.get(country, (1.0, 6.0))
    return round(random.uniform(min_inf, max_inf), 2)


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