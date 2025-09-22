# banrep_api.py
"""
API integration module for Banco de la República de Colombia
"""
import requests
import json
from datetime import datetime, timedelta


class BanRepAPI:
    """Clase para manejar la integración con las APIs del Banco de la República."""
    
    def __init__(self):
        """Inicializa el cliente de la API del Banco de la República."""
        self.base_url = "https://tutorials.banrep.gov.co/api/v1"
        self.session = requests.Session()
        
    def get_trm(self, date=None):
        """
        Obtiene el TRM (Tasa de Cambio Representativa del Mercado).
        
        Args:
            date (str): Fecha específica en formato YYYY-MM-DD (opcional)
            
        Returns:
            dict: Datos del TRM
        """
        try:
            if date:
                url = f"{self.base_url}/series/TRM/date/{date}"
            else:
                url = f"{self.base_url}/series/TRM/latest"
                
            response = self.session.get(url)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error al obtener TRM: {e}")
            return None
    
    def get_trm_history(self, start_date=None, end_date=None, days=45):
        """
        Obtiene el historial de TRM.
        
        Args:
            start_date (str): Fecha de inicio en formato YYYY-MM-DD
            end_date (str): Fecha de fin en formato YYYY-MM-DD
            days (int): Número de días hacia atrás si no se especifican fechas
            
        Returns:
            dict: Historial de TRM
        """
        try:
            url = f"{self.base_url}/series/TRM/history"
            params = {}
            
            if start_date:
                params['start_date'] = start_date
            if end_date:
                params['end_date'] = end_date
            if not start_date and not end_date:
                params['days'] = days
                
            response = self.session.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error al obtener historial de TRM: {e}")
            return None
    
    def get_inflation(self, year=None, month=None):
        """
        Obtiene datos de inflación (IPC - Índice de Precios al Consumidor).
        
        Args:
            year (int): Año específico (opcional)
            month (int): Mes específico (opcional)
            
        Returns:
            dict: Datos de inflación
        """
        try:
            if year and month:
                url = f"{self.base_url}/series/IPC/{year}/{month}"
            elif year:
                url = f"{self.base_url}/series/IPC/{year}"
            else:
                url = f"{self.base_url}/series/IPC/latest"
                
            response = self.session.get(url)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error al obtener inflación: {e}")
            return None
    
    def get_interest_rate(self, date=None):
        """
        Obtiene la Tasa de Intervención del Banco de la República.
        
        Args:
            date (str): Fecha específica en formato YYYY-MM-DD (opcional)
            
        Returns:
            dict: Datos de la tasa de interés
        """
        try:
            if date:
                url = f"{self.base_url}/series/TI/date/{date}"
            else:
                url = f"{self.base_url}/series/TI/latest"
                
            response = self.session.get(url)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error al obtener tasa de interés: {e}")
            return None
    
    def get_indicator(self, indicator_id, start_date=None, end_date=None):
        """
        Obtiene un indicador económico específico.
        
        Args:
            indicator_id (str): ID del indicador
            start_date (str): Fecha de inicio en formato YYYY-MM-DD (opcional)
            end_date (str): Fecha de fin en formato YYYY-MM-DD (opcional)
            
        Returns:
            dict: Datos del indicador
        """
        try:
            url = f"{self.base_url}/series/{indicator_id}"
            params = {}
            
            if start_date:
                params['start_date'] = start_date
            if end_date:
                params['end_date'] = end_date
                
            response = self.session.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error al obtener indicador {indicator_id}: {e}")
            return None


# Funciones de conveniencia
def get_banrep_data(indicator_id, **kwargs):
    """
    Obtiene datos de un indicador del Banco de la República.
    
    Args:
        indicator_id (str): ID del indicador (TRM, IPC, TI, etc.)
        **kwargs: Parámetros adicionales para la consulta
        
    Returns:
        dict: Datos del indicador
    """
    api = BanRepAPI()
    return api.get_indicator(indicator_id, **kwargs)


def get_colombian_trm(date=None):
    """
    Obtiene el TRM colombiano.
    
    Args:
        date (str): Fecha específica en formato YYYY-MM-DD (opcional)
        
    Returns:
        float: Valor del TRM
    """
    api = BanRepAPI()
    data = api.get_trm(date)
    if data and 'value' in data:
        return float(data['value'])
    return None


def get_colombian_inflation(year=None, month=None):
    """
    Obtiene la inflación colombiana.
    
    Args:
        year (int): Año específico (opcional)
        month (int): Mes específico (opcional)
        
    Returns:
        float: Tasa de inflación
    """
    api = BanRepAPI()
    data = api.get_inflation(year, month)
    if data and 'value' in data:
        return float(data['value'])
    return None